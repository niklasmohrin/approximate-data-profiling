#!/usr/bin/env python3

import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
    dfs = list(map(pd.read_json, sys.stdin.readlines()))
    for df in dfs:
        method = df.columns[0]
        df: pd.DataFrame
        df.rename(columns={method: "error"}, inplace=True)
        df["method"] = method

    data: pd.DataFrame = pd.concat(dfs)
    data["method"] = data["method"].astype("category")

    _, axs = plt.subplots(ncols=2)
    sns.violinplot(data=data, x="error", y="method", cut=0, scale="count", ax=axs[0])
    axs[0].set_title("Scale: Count")
    sns.violinplot(data=data, x="error", y="method", cut=0, scale="width", ax=axs[1])
    axs[1].set_title("Scale: Width")
    plt.show()


if __name__ == "__main__":
    main()
