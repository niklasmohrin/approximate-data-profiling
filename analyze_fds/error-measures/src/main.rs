use std::{collections::HashMap, fs, io};

use clap::Parser;
use polars::prelude::*;
use serde::Deserialize;

mod cli;
mod stripped_partition;

use cli::{Cli, Command};
use stripped_partition::StrippedPartition;

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
    let mut stripped_partition_of = |cols: Vec<String>| -> StrippedPartition {
        cache
            .entry(cols)
            .or_insert_with_key(|cols| {
                let mut col_parts = base_partitions
                    .iter()
                    .filter(|p| cols.contains(p.columns.iter().next().unwrap()));
                let initial = col_parts.next().unwrap().clone();
                col_parts.fold(initial, |a, b| a.product_in(b, &full_df))
            })
            .clone()
    };

    for fd_path in args.fd_path.iter() {
        let fd_file = fs::read_to_string(fd_path)?;
        let fds: Vec<Line> = fd_file
            .lines()
            .map(serde_json::from_str)
            .collect::<Result<_, _>>()?;

        let error_counts = fds.into_iter().map(|fd| {
            let mut error = 0;
            let x_part = stripped_partition_of(
                fd.determinant
                    .column_identifiers
                    .iter()
                    .map(|ident| ident.column_identifier.clone())
                    .collect::<Vec<_>>(),
            );
            let a_part = stripped_partition_of(vec![fd.dependant.column_identifier]);
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

        match args.command {
            Command::ErrorSummary => {
                let median_error = errors.median().unwrap();
                let error_df = DataFrame::new(vec![errors])?;
                let stats = error_df.describe(None);
                let stats =
                    stats.vstack(&df! { "describe" => ["median"], "error" => [median_error]}?)?;
                println!("{}", stats);
            }
            Command::OutputErrors => {
                let mut error_df = df! {
                    fd_path.file_name().unwrap().to_str().unwrap() => [errors],
                }
                .unwrap();
                JsonWriter::new(io::stdout()).finish(&mut error_df)?;
            }
        }
    }

    Ok(())
}
