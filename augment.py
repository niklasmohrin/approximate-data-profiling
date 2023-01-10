#!/usr/bin/env python3

import argparse
from enum import Enum, auto
from pathlib import Path

import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE, SMOTEN, SMOTENC
from sklearn.preprocessing import OneHotEncoder


class Method(Enum):
    smote = auto()
    smoten = auto()
    smotenc = auto()
    # Adasyn = auto()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", choices=[m.name for m in Method])
    parser.add_argument("--factor", type=float)
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    df = pd.read_csv(args.path, sep=";")
    out_size = int(len(df) * args.factor)
    print(f"{len(df)=} {out_size=}")

    num_df = df.select_dtypes(include="number")
    string_df = df.select_dtypes(exclude="number")
    encoder = OneHotEncoder().fit(string_df)
    match Method[args.method]:
        case Method.smote:
            onehot_columns = encoder.get_feature_names_out(string_df.columns)
            string_df_onehot = pd.DataFrame.sparse.from_spmatrix(
                encoder.transform(string_df),
                columns=onehot_columns,
            )
            x = pd.concat([num_df, string_df_onehot], axis=1)
            x.loc[len(x)] = x.iloc[len(x) - 1]
            y = np.zeros((len(x), 1))
            y[len(y) - 1] = 1
            out_x, out_y = SMOTE(
                sampling_strategy={0: int(args.factor * len(df)), 1: 1}
            ).fit_resample(x.to_numpy(), y)
            out_x = out_x[out_y == 0]
            out_df = pd.DataFrame(out_x, columns=x.columns)
            out_df = pd.concat(
                [
                    out_df.drop(columns=onehot_columns),
                    pd.DataFrame(
                        encoder.inverse_transform(out_df[onehot_columns]),
                        columns=string_df.columns,
                    ),
                ],
                axis=1,
            )
        case Method.smotenc:
            x = df.copy()
            x.loc[len(x)] = x.iloc[len(x) - 1]
            y = np.zeros((len(x), 1))
            y[len(y) - 1] = 1
            out_x, out_y = SMOTENC(
                categorical_features=[col in string_df.columns for col in x.columns],
                sampling_strategy={0: int(args.factor * len(df)), 1: 1},
            ).fit_resample(x, y)
            out_x = out_x[out_y == 0]
            out_df = pd.DataFrame(out_x, columns=x.columns)
        case Method.smoten:
            x = df.copy()
            x.loc[len(x)] = x.iloc[len(x) - 1]
            y = np.zeros((len(x), 1))
            y[len(y) - 1] = 1
            out_x, out_y = SMOTEN(
                sampling_strategy={0: int(args.factor * len(df)), 1: 1},
            ).fit_resample(x, y)
            out_x = out_x[out_y == 0]
            out_df = pd.DataFrame(out_x, columns=x.columns)
        case _:
            raise NotImplementedError

    print(f"{len(out_df)=}")
    out_path = f"{args.path.name.removesuffix('.csv')}_{args.method}_{args.factor}.csv"
    out_df.to_csv(
        out_path,
        sep=";",
        index=False,
    )
    print(out_path)


if __name__ == "__main__":
    main()
