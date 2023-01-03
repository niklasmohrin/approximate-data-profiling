#!/usr/bin/env python3

import csv
import errno
import itertools
import os
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path



@dataclass
class Dataset:
    name: str
    filename: str
    separator: str = ";"


AdultsDataset = Dataset("adults", "adult.csv")
FDR30Dataset = Dataset("fdr30", "fdr30.csv", separator=",")
LetterDataset = Dataset("letter", "letter.csv", separator=",")
Plista1K = Dataset("plista1k", "plista_1k.csv")
TPCHLineItem = Dataset("tpc-lineitem", "TPC-H/tpch_lineitem.csv")
TPCHCustomer = Dataset("tpc-customer", "TPC-H/tpch_customer.csv")
TPCHOrder = Dataset("tpc-orders", "TPC-H/tpch_orders.csv")
TPCHOrdersCustomer = Dataset("tpc-orders-customer", "TPC-H/tpch_orders_customer.csv")


datasets = [
    TPCHOrdersCustomer,
    AdultsDataset,
]
dataset = datasets[0]
# Constants
data_dir = "source"
results_dir = "results"

METANOME_CLI_LOCATION = "metanome/cli.jar"
METANOME_ALGORITHM_LOCATION = "metanome/hyfd.jar"

# Cmds
build_sample_cmd = (
    lambda m, f, table: f"python sample.py --method {m} --factor {f} {table}"
)


def build_metanome_cmd(table_path: str, output_path: str, separator: str):
    return f"""java -Dtinylog.level=trace \
        -cp {METANOME_CLI_LOCATION}:{METANOME_ALGORITHM_LOCATION} de.metanome.cli.App \
        --algorithm de.metanome.algorithms.hyfd.HyFD \
        --files {table_path} --file-key INPUT_GENERATOR \
        --header --separator "{separator}"\
        -o file:{output_path}
    """


def build_fd_error_cmd(
    mode: str, table_path: str, fd_jsons: list[Path], out_file: str = "errors.json"
):
    return f"""cargo run --manifest-path analyze_fds/error-measures/Cargo.toml --release -- '{str(table_path)}' {mode} '{"' '".join(map(str, fd_jsons))}' > {out_file}"""


def build_violin_plot_cmd(errors_json_path: str):
    return f"cat {errors_json_path} | ./analyze_fds/error-measures/violin_plot.py"


build_mv_cmd = lambda old_path, new_path: f"mv {str(old_path)} {str(new_path)}"

build_plot_cmd = (
    lambda fd_json_sources: f"python analyze_fds/fd_count/src/main.py --save --data-sources {' '.join(map(str, fd_json_sources))}"
)


def build_uniqueness_cmd(experiment_dir: str):
    return f"""
        python analyze_fds/fd_count/src/unique_values.py -s "{str(experiment_dir)}"
        python analyze_fds/fd_count/src/plot_uniques.py -s {os.path.join(str(experiment_dir), "uniques.csv")}
    """


def run_cmd_get_last_line(cmd: str):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    # TODO: this is synchronous, so not working for large pipes...
    out, err = p.communicate()
    # Output ends with \n, so we need second last line
    return out.decode().split("\n")[-2]


def runShell(cmd: str):
    return subprocess.run(cmd, shell=True)


def create_results_dir(folder_name: str):
    mydir = os.path.join(
        os.getcwd(),
        results_dir,
        datetime.now().strftime(f"%Y-%m-%d_%H-%M-%S_{folder_name}"),
    )
    try:
        os.makedirs(mydir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    return mydir


def main():
    experiment_dir = create_results_dir(dataset.name)
    source_table = os.path.join(data_dir, dataset.filename)

    # Rewrite separator, if not the default
    if dataset.separator != Dataset.separator:
        bak_path = source_table + ".bak"
        if not os.path.exists(bak_path):
            runShell(build_mv_cmd(source_table, bak_path))
            reader = csv.reader(
                open(bak_path, newline=None), delimiter=dataset.separator
            )
            writer = csv.writer(open(source_table, "w"), delimiter=Dataset.separator)
            writer.writerows(reader)
        dataset.separator = Dataset.separator

    sample_methods = ["full", "random"]  # , "kmeans"
    sample_factors = [0.01, 0.1, 1]
    # sample_factors = [1]

    sample_paths: list[Path] = []
    fd_paths: list[Path] = []

    def mv_to_results(file_path: str, new_name: str = None) -> Path:
        src_path = Path(file_path)
        target_path = Path(
            experiment_dir, new_name if new_name is not None else src_path.name
        )

        subprocess.run(build_mv_cmd(str(src_path), str(target_path)), shell=True)
        return target_path

    ### Evaluation for each sampling method ###
    for method, factor in itertools.product(sample_methods, sample_factors):
        # Only 
        if method != "full" and factor == 1 or method == "full" and factor != 1:
            continue

        print(f"Sample {method} with {factor}")
        # TODO: Active when names would be not unique / count?
        run_time_str = ""  # f"{datetime.now().strftime(f"%Y-%m-%d_%H-%M-%S")}_"
        # Sample something
        if method != "full":
            sample_path = Path(
                run_cmd_get_last_line(build_sample_cmd(method, factor, source_table))
            )
        else:
            sample_path = Path(experiment_dir, 'full.csv')
            runShell(f"cp {source_table} {sample_path}")

        if not os.path.exists(sample_path):
            print(f"Sampling {method} @ {factor} failed. Skipping.")
            continue

        # Move sample to unique location
        new_sample_name = f"{run_time_str}{sample_path.name}"
        new_sample_path = mv_to_results(sample_path, new_sample_name)
        sample_paths.append(new_sample_path)

        # Run Metanome for FD Detection
        fd_file_name = f"{run_time_str}{sample_path.stem}"
        runShell(build_metanome_cmd(new_sample_path, fd_file_name, dataset.separator))

        # Metanome appends _fds to file name
        fd_file_after_metanome = Path("results", f"{fd_file_name}_fds")
        fd_file_path = mv_to_results(fd_file_after_metanome)
        fd_paths.append(fd_file_path)

    ### Evaluations for all sampling methods / Comparison ###
    errors_json_path = os.path.join(experiment_dir, "errors.json")
    runShell(
        build_fd_error_cmd("output-errors", source_table, fd_paths, errors_json_path)
    )
    clusters_path = os.path.join(experiment_dir, "clusters.json")
    runShell(
        build_fd_error_cmd("output-cluster-sizes", source_table, fd_paths, clusters_path)
    )

    runShell(build_violin_plot_cmd(errors_json_path))
    mv_to_results("violinplot.pdf")

    # save fd_count plot
    plot_cmd = build_plot_cmd(fd_paths)
    plot_file_path = Path(run_cmd_get_last_line(plot_cmd))
    runShell(
        build_mv_cmd(
            str(plot_file_path), os.path.join(experiment_dir, plot_file_path.name)
        )
    )

    # Save uniqueness plots
    runShell(build_uniqueness_cmd(experiment_dir))


if __name__ == "__main__":
    for ds in datasets:
        dataset = ds
        main()
