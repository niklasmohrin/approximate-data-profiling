#!/usr/bin/env python3

import itertools
import os
import subprocess
from pathlib import Path
from Dataset import Dataset
from commands import *
from constants import *


AdultsDataset = Dataset("adults", "adult.csv")
FDR30Dataset = Dataset("fdr30", "fdr30.csv", separator=",")
LetterDataset = Dataset("letter", "letter.csv", separator=",")
Plista1K = Dataset("plista1k", "plista_1k.csv")
TPCHLineItem = Dataset("tpc-lineitem", "TPC-H/tpch_lineitem.csv")
TPCHCustomer = Dataset("tpc-customer", "TPC-H/tpch_customer.csv")
TPCHOrder = Dataset("tpc-orders", "TPC-H/tpch_orders.csv")
TPCHOrdersCustomer = Dataset("tpc-orders-customer", "TPC-H/tpch_orders_customer.csv")


datasets = [AdultsDataset]
dataset = datasets[0]


def main():
    experiment_dir = create_results_dir(dataset.name)
    source_table = os.path.join(DATA_DIR, dataset.filename)

    # Rewrite separator, if not the default
    if dataset.separator != Dataset.separator:
        rewrite_separator(dataset, source_table)

    sample_methods = ["full", "random"]  # , "kmeans"
    sample_factors = [0.01, 1]
    sample_iterations = range(10)
    augmentation_method = 'smotenc'
    augmentation_factor = 10.0
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
    for method, factor, iteration in itertools.product(sample_methods, sample_factors, sample_iterations):
        # Only
        if method != "full" and factor == 1 or method == "full" and factor != 1 or method == "full" and iteration != 0:
            continue

        print(f"Sample {method} with {factor}")
        # TODO: Active when names would be not unique / count?
        run_time_str = f"{iteration}_" if len(sample_iterations) > 1 else ""
        sample_path = sample_with_method(method, factor, experiment_dir, source_table)
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

        if method == 'full':
            continue
        
        ### Evaluation for all augmentation methods ###
        for idx in range(1):
            print(f'Augmenting data')
            base_file_name = f'{new_sample_path.stem}_{augmentation_method}x{augmentation_factor}'

            augmentation_path = augment_with_method(augmentation_method, augmentation_factor, experiment_dir, new_sample_path)
            augmentation_path = mv_to_results(augmentation_path, base_file_name + '.csv')

            fd_file_name = base_file_name
            runShell(build_metanome_cmd(augmentation_path, fd_file_name, dataset.separator))

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
        build_fd_error_cmd(
            "output-cluster-sizes", source_table, fd_paths, clusters_path
        )
    )

    runShell(build_violin_plot_cmd(errors_json_path))
    mv_to_results("violinplot.pdf")

    # save fd_count plot
    plot_cmd = build_plot_cmd(fd_paths)
    print(plot_cmd)
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
