#!/usr/bin/env python3

import argparse
from pathlib import Path

import pandas as pd
from sklearn.cluster import k_means
from sklearn.preprocessing import OrdinalEncoder


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", choices=["random", "kmeans"])
    parser.add_argument("--factor", type=float)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    df = pd.read_csv(args.path, sep=";", header=None)
    out_size = int(len(df) * args.factor)
    print(f"{len(df)=} {out_size=}")

    match args.method:
        case "random":
            out_df = df.sample(out_size)
        case "kmeans":
            string_df = df.select_dtypes(exclude="number")
            string_cols = string_df.columns
            num_df = df.copy()
            num_df[string_cols] = OrdinalEncoder().fit_transform(string_df)
            # "Random" value to override missing values for kmeans sampling
            num_df.fillna(-9898989, inplace=True)

            _centroids, labels, _inertia = k_means(num_df, out_size)
            indices = [-1] * out_size
            for i, label in enumerate(labels):
                indices[label] = i
            out_df = df.iloc[indices]

    print(f"{len(out_df)=}")
    out_path = f"{args.path.name.removesuffix('.csv')}_{args.method}_{args.factor}.csv"
    out_df.to_csv(
        out_path,
        header=None,
        sep=";",
        index=False,
    )
    print(out_path)


if __name__ == "__main__":
    main()
