use std::{
    collections::{HashMap, HashSet},
    env, fs, mem,
};

use anyhow::bail;
use polars::prelude::*;
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
        .map(|column| {
            let groups = full_df.groupby([column.name()]).unwrap().groups().unwrap();
            let groups: Vec<HashSet<usize>> = groups
                .column("groups")
                .unwrap()
                .list()
                .unwrap()
                .into_no_null_iter()
                .filter(|series| series.len() > 1)
                .map(|series| {
                    series
                        .u32()
                        .unwrap()
                        .into_no_null_iter()
                        .map(|x| x as usize)
                        .collect()
                })
                .collect();

            StrippedPartition {
                columns: HashSet::from([column.name().to_owned()]),
                partitions: groups,
            }
        })
        .collect();

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
        .map(|line| serde_json::from_str(line))
        .collect::<Result<_, _>>()?;

    let mut error_counts: Vec<usize> = fds
        .into_iter()
        .map(|fd| {
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
        })
        .collect();

    error_counts.sort_unstable();
    for error_count in error_counts {
        println!(
            "Fd has {} wrong rows, error is {}",
            error_count,
            error_count as f64 / full_df.height() as f64
        );
    }

    Ok(())
}
