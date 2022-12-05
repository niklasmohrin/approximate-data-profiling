use std::path::PathBuf;

use clap::{Parser, Subcommand};

#[derive(Debug, Parser)]
#[command(author, version, about, long_about = None)]
pub struct Cli {
    pub relation_path: PathBuf,
    #[command(subcommand)]
    pub command: Command,
}

#[derive(Debug, Clone, Subcommand)]
pub enum Command {
    ErrorSummary {
        fds: Vec<PathBuf>,
    },
    OutputErrors {
        fds: Vec<PathBuf>,
    },
    OutputApproximationMetrics {
        gold_fd_path: PathBuf,
        fds: Vec<PathBuf>,
    },
    OutputClusterSizes {
        fds: Vec<PathBuf>,
    },
}

impl Command {
    pub fn fds(&self) -> &[PathBuf] {
        match self {
            Self::ErrorSummary { fds }
            | Self::OutputErrors { fds }
            | Self::OutputApproximationMetrics { fds, .. }
            | Self::OutputClusterSizes { fds } => fds,
        }
    }
}
