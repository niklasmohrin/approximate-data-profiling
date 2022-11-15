use std::path::PathBuf;

use clap::{Parser, ValueEnum};

#[derive(Debug, Parser)]
#[command(author, version, about, long_about = None)]
pub struct Cli {
    #[arg(value_enum)]
    pub command: Command,
    pub relation_path: PathBuf,
    pub fd_path: Vec<PathBuf>,
}

#[derive(Debug, Clone, Copy, ValueEnum)]
pub enum Command {
    ErrorSummary,
    OutputErrors,
}
