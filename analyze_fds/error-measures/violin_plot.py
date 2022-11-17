#!/usr/bin/env python3

import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
    dfs = list(map(pd.read_json, sys.stdin.readlines()))
    for df in dfs:
        method = df.columns[0]
        df.rename(columns={method: "error"}, inplace=True)
        df["method"] = method

    data: pd.DataFrame = pd.concat(dfs)
    data["method"] = data["method"].astype("category")

    _, axs = plt.subplots(ncols=2, figsize=(17, 7))
    for ax, scale in zip(axs, ["count", "width"]):
        sns.violinplot(data=data, x="error", y="method", cut=0, scale=scale, ax=ax)
        ax.set_title(f"Scale: {scale}")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
