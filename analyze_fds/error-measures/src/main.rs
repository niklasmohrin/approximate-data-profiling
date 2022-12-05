use std::{
    collections::{HashMap, HashSet},
    fs,
    io::{self, BufWriter},
    path::Path,
};

use clap::Parser;
use polars::prelude::*;
use serde::{Deserialize, Serialize};

mod cli;
mod stripped_partition;

use cli::{Cli, Command};
use stripped_partition::StrippedPartition;

#[derive(Debug, Clone, Serialize, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "camelCase")]
struct Identifier {
    column_identifier: String,
}
#[derive(Debug, Clone, Deserialize, PartialEq, Eq, Hash)]
#[serde(rename_all = "camelCase")]
struct Determinant {
    column_identifiers: Vec<Identifier>,
}

#[derive(Debug, Clone, Deserialize, PartialEq, Eq, Hash)]
struct FdLine {
    determinant: Determinant,
    dependant: Identifier,
}

fn main() -> anyhow::Result<()> {
    let args = Cli::parse();

    let full_df = CsvReader::from_path(args.relation_path)?
        .with_delimiter(b';')
        .finish()?
        .with_row_count("id", None)?;

    let base_partitions: Vec<StrippedPartition> = full_df
        .iter()
        .map(|column| StrippedPartition::new_for_column_in(column.name(), &full_df))
        .collect::<Result<_, _>>()?;

    let mut cache = HashMap::<Vec<String>, StrippedPartition>::new();
    let stripped_partition_of = |cols: Vec<String>,
                                 cache: &mut HashMap<Vec<String>, StrippedPartition>|
     -> StrippedPartition {
        cache
            .entry(cols)
            .or_insert_with_key(|cols| {
                let col_parts = base_partitions
                    .iter()
                    .filter(|p| cols.contains(p.columns.iter().next().unwrap()));
                let initial = StrippedPartition::new_initial_for(full_df.height());
                col_parts.fold(initial, |a, b| a.product_in(b, &full_df))
            })
            .clone()
    };

    let error_of = |fd: &FdLine, partition_cache: &mut HashMap<Vec<String>, StrippedPartition>| {
        let mut error = 0;
        let x_part = stripped_partition_of(
            fd.determinant
                .column_identifiers
                .iter()
                .map(|ident| ident.column_identifier.clone())
                .collect::<Vec<_>>(),
            partition_cache,
        );
        let a_part = stripped_partition_of(
            vec![fd.dependant.column_identifier.clone()],
            partition_cache,
        );
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
    };

    for fd_path in args.command.fds().iter() {
        let fds = read_fds_from_file(fd_path)?;

        match &args.command {
            Command::ErrorSummary { .. } => {
                let error_counts = fds.iter().map(|fd| error_of(fd, &mut cache));
                let errors = error_counts.map(|error| error as f64 / full_df.height() as f64);
                let errors = Series::new("error", errors.collect::<Vec<_>>());
                let median_error = errors.median().unwrap();
                let error_df = DataFrame::new(vec![errors])?;
                let stats = error_df.describe(None);
                let stats =
                    stats.vstack(&df! { "describe" => ["median"], "error" => [median_error]}?)?;
                println!("{}", stats);
            }
            Command::OutputErrors { .. } => {
                let error_counts = fds.iter().map(|fd| error_of(fd, &mut cache));
                let errors = error_counts.map(|error| error as f64 / full_df.height() as f64);
                let errors = Series::new("error", errors.collect::<Vec<_>>());
                let mut error_df = df! {
                    fd_path.file_name().unwrap().to_str().unwrap() => [errors],
                }
                .unwrap();
                JsonWriter::new(io::stdout()).finish(&mut error_df)?;
            }
            Command::OutputApproximationMetrics { gold_fd_path, .. } => {
                let gold = read_fds_from_file(&gold_fd_path)?;

                let gold_set: HashSet<FdLine> = HashSet::from_iter(gold.iter().cloned());
                let discovered_gold_fd_count =
                    fds.iter().filter(|fd| gold_set.contains(fd)).count();
                let completeness = discovered_gold_fd_count as f64 / gold.len() as f64;

                let error_counts = fds.iter().map(|fd| error_of(fd, &mut cache));
                let correct_fd_count = error_counts.filter(|&err| err == 0).count();
                let correctness = correct_fd_count as f64 / fds.len() as f64;

                println!("File: {}", fd_path.display());
                println!("  Completeness: {}", completeness);
                println!("  Correctness:  {}", correctness);
            }
            Command::OutputClusterSizes { .. } => {
                let mut determinant_cluster_sizes = HashMap::new();
                let mut dependant_cluster_sizes = HashMap::new();
                for fd in fds {
                    stripped_partition_of(
                        fd.determinant
                            .column_identifiers
                            .iter()
                            .map(|ident| ident.column_identifier.clone())
                            .collect(),
                        &mut cache,
                    )
                    .add_cluster_size_counts_to(&mut determinant_cluster_sizes, full_df.height());
                    stripped_partition_of(vec![fd.dependant.column_identifier.clone()], &mut cache)
                        .add_cluster_size_counts_to(&mut dependant_cluster_sizes, full_df.height());
                }
                let mut determinant_cluster_sizes: Vec<_> =
                    determinant_cluster_sizes.into_iter().collect();
                determinant_cluster_sizes.sort_unstable();
                let mut dependant_cluster_sizes: Vec<_> =
                    dependant_cluster_sizes.into_iter().collect();
                dependant_cluster_sizes.sort_unstable();
                #[derive(Debug, Serialize)]
                struct Out<'a> {
                    fd_path: &'a Path,
                    determinant_cluster_sizes: Vec<(usize, usize)>,
                    dependant_cluster_sizes: Vec<(usize, usize)>,
                }
                serde_json::to_writer(
                    BufWriter::new(io::stdout().lock()),
                    &Out {
                        fd_path,
                        determinant_cluster_sizes,
                        dependant_cluster_sizes,
                    },
                )?;
                println!();
            }
        }
    }

    Ok(())
}

fn read_fds_from_file(path: &Path) -> anyhow::Result<Vec<FdLine>> {
    let fd_file = fs::read_to_string(path)?;
    Ok(fd_file
        .lines()
        .map(serde_json::from_str)
        .collect::<Result<_, _>>()?)
}
