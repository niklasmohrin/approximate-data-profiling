#!/usr/bin/env python3

import json
import sys

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np


def plot_clusters(method, tuple_list):
    # save the names and their respective scores separately
    # reverse the tuples to go from most frequent to least frequent
    size = list(zip(*tuple_list))[0]
    count = list(zip(*tuple_list))[1]
    x_pos = np.arange(len(size))
    print(size)
    plt.bar(x_pos, count, align="center")
    plt.xticks(x_pos, size)
    plt.xscale("log")
    plt.ylabel("Number of clusters")

    plt.title(method)
    plt.savefig(method + "_clusters.pdf")


def main():
    dfs_json = list(map(json.loads, sys.stdin.readlines()))
    for df_json in dfs_json:
        method = df_json["fd_path"]
        data_tuples = df_json["determinant_cluster_sizes"]
        plot_clusters(method, data_tuples)

    # data: pd.DataFrame = pd.concat(dfs)
    # data["method"] = data["method"].astype("category")

    # _, axs = plt.subplots(ncols=2, figsize=(17, 7))
    # for ax, scale in zip(axs, ["count", "width"]):
    #     sns.violinplot(data=data, x="error", y="method", cut=0, scale=scale, ax=ax)
    #     ax.set_title(f"Scale: {scale}")

    # plt.tight_layout()
    # plt.savefig('violinplot.pdf')


if __name__ == "__main__":
    main()
