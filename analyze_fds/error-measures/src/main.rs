use std::{
    collections::{HashMap, HashSet},
    env, fs, mem,
};

use anyhow::bail;
use polars::prelude::*;
use rayon::prelude::*;
use serde::Deserialize;

#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct Identifier {
    column_identifier: String,
}
#[derive(Debug, Deserialize)]
#[serde(rename_all = "camelCase")]
struct Determinant {
    column_identifiers: Vec<Identifier>,
}

#[derive(Debug, Deserialize)]
struct Line {
    determinant: Determinant,
    dependant: Identifier,
}

#[derive(Debug, Clone)]
struct StrippedPartition {
    columns: HashSet<String>,
    partitions: Vec<HashSet<usize>>,
}

impl StrippedPartition {
    pub fn new_for_column_in(column_name: &str, relation: &DataFrame) -> anyhow::Result<Self> {
        let groups = relation
            .groupby([column_name])?
            .take_groups()
            .as_list_chunked();
        let non_trivial = groups.lst_lengths().gt(1);

        let partitions: Vec<HashSet<usize>> = groups
            .filter(&non_trivial)?
            .par_iter()
            .map(|index_series| {
                index_series
                    .expect("Index series should not be null")
                    .u32()
                    .expect("Index series should have u32 dtype.")
                    .into_no_null_iter()
                    .map(|index| index.try_into().unwrap())
                    .collect()
            })
            .collect();

        Ok(Self {
            columns: HashSet::from([column_name.to_owned()]),
            partitions,
        })
    }

    pub fn product_in(&self, other: &Self, relation: &DataFrame) -> Self {
        let mut partitions = Vec::new();

        let mut s = vec![HashSet::new(); self.partitions.len()];
        let mut t = vec![None; relation.height()];
        for (i, partition) in self.partitions.iter().enumerate() {
            for &tuple in partition.iter() {
                t[tuple] = Some(i);
            }
        }
        for partition in other.partitions.iter() {
            for &tuple in partition.iter() {
                if let Some(index) = t[tuple] {
                    s[index].insert(tuple);
                }
            }
            for &tuple in partition.iter() {
                if let Some(index) = t[tuple] {
                    let p = mem::take(&mut s[index]);
                    if p.len() >= 2 {
                        partitions.push(p);
                    }
                }
            }
        }

        Self {
            columns: self.columns.union(&other.columns).cloned().collect(),
            partitions,
        }
    }
}

fn main() -> anyhow::Result<()> {
    let mut args = env::args();
    let _ = args.next();
    let (Some(full_data_path), Some(fds_path)) = (args.next(), args.next()) else {
        bail!("Usage");
    };

    let full_df = CsvReader::from_path(full_data_path)?
        .with_delimiter(b';')
        .finish()?
        .with_row_count("id", None)?;

    let base_partitions: Vec<StrippedPartition> = full_df
        .iter()
        .map(|column| StrippedPartition::new_for_column_in(column.name(), &full_df))
        .collect::<Result<_, _>>()?;

    let stripped_partition_of = |cols: &[&str]| -> StrippedPartition {
        let mut col_parts = base_partitions
            .iter()
            .filter(|p| cols.contains(&p.columns.iter().next().unwrap().as_str()));
        let initial = col_parts.next().unwrap().clone();
        col_parts.fold(initial, |a, b| a.product_in(b, &full_df))
    };

    let fd_file = fs::read_to_string(fds_path)?;
    let fds: Vec<Line> = fd_file
        .lines()
        .map(serde_json::from_str)
        .collect::<Result<_, _>>()?;

    let error_counts = fds.into_iter().map(|fd| {
        let mut error = 0;
        let x_part = stripped_partition_of(
            &fd.determinant
                .column_identifiers
                .iter()
                .map(|ident| ident.column_identifier.as_str())
                .collect::<Vec<_>>(),
        );
        let a_part = stripped_partition_of(&[&fd.dependant.column_identifier]);
        let xa_part = x_part.product_in(&a_part, &full_df);
        let mut t: HashMap<usize, usize> = HashMap::new();
        for partition in xa_part.partitions.into_iter() {
            let &tuple = partition.iter().next().unwrap();
            t.insert(tuple, partition.len());
        }
        for partition in x_part.partitions.into_iter() {
            error += partition.len();
            let m = partition
                .into_iter()
                .flat_map(|tuple| t.get(&tuple).copied())
                .max()
                .unwrap_or(1);
            error -= m;
        }

        error
    });

    let errors = error_counts.map(|error| error as f64 / full_df.height() as f64);
    let errors = Series::new("error", errors.collect::<Vec<_>>());
    let median_error = errors.median().unwrap();
    let error_df = DataFrame::new(vec![errors])?;
    let stats = error_df.describe(None);
    let stats = stats.vstack(&df! { "describe" => ["median"], "error" => [median_error]}?)?;
    println!("{}", stats);

    Ok(())
}
