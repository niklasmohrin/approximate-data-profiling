#!/usr/bin/env python3

import os
from argparse import ArgumentParser

import pandas as pd
from load import load_fd_list


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-s",
        "--data-source",
        help="Path to files to plot",
    )
    args = parser.parse_args()

    result_df = pd.DataFrame(
        columns=[
            "method",
            "determinants",
            "dependant",
            "uniques_determinant",
            "uniques_dependant",
            "error",
        ]
    )

    # Load FDs
    with open(os.path.join(args.data_source, "errors.json")) as error_file,  open(os.path.join(args.data_source, "clusters.json")) as clusters_file:
        error_dfs = list(map(pd.read_json, error_file.readlines()))
        # cluster_dfs = list(map(pd.read_json, clusters_file.readlines()))
        # for error_df, cluster_df in zip(error_dfs, cluster_dfs):
        for error_df in error_dfs:
            method = error_df.columns[0]
            error_df.rename(columns={method: "error"}, inplace=True)
            # cluster_df.rename(columns={method: "determinant_cluster_size"}, inplace=True)

            fd_file: str = os.path.join(args.data_source, method)
            fds = load_fd_list(fd_file)

            source_file = fd_file.removesuffix("_fds") + ".csv"
            source = pd.read_csv(source_file, sep=";")
            #rename_dict = {k: f"column{k+1}" for k in source.columns}
            #source.rename(rename_dict, inplace=True, axis=1)

            total_rows = len(source)

            cache = {}

            def get_uniques(source: pd.DataFrame, columns: list[str]):
                col_id = "_".join(columns)
                if cache.get(col_id) is None:
                    # Edge case: if columns is empty, we didnt need any determinant, so the "uniqueness" of the determinant is 0
                    cache[col_id] = (
                        0 if len(columns) == 0 else len(source[columns].value_counts())
                    )
                return cache[col_id]

            def get_uniques_sum_per_col(source: pd.DataFrame, columns: list[str]):
                uniques = sum(map(lambda col: get_uniques(source, [col]), columns))
                return uniques

            for idx, fd in enumerate(fds):
                if idx % 1000 == 0:
                    print(f"Running... {idx}")
                dependant, determinants = fd
                # uniques_determinant = get_uniques(source, determinants) / total_rows
                uniques_determinant = get_uniques_sum_per_col(source, determinants) / total_rows
                uniques_dependant = get_uniques(source, [dependant]) / total_rows
                error = error_df.iloc[idx, 0]
                # cluster_size = cluster_df.iloc[idx, 0]

                result_df = pd.concat(
                    [
                        result_df,
                        pd.DataFrame.from_records(
                            [
                                {
                                    "method": method,
                                    "determinants": determinants,
                                    "dependant": dependant,
                                    "uniques_determinant": uniques_determinant,
                                    # "determinant_cluster_size": cluster_size,
                                    "uniques_dependant": uniques_dependant,
                                    "error": error,
                                }
                            ]
                        ),
                    ],
                    ignore_index=True,
                )
            # print(error_df)
        # Load Source
        # Load errors
    result_df.to_csv(os.path.join(args.data_source, "uniques.csv"), index=False)

    result_df.plot(x="method", y="uniques_determinant")


if __name__ == "__main__":
    main()
