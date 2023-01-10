from argparse import ArgumentParser
from pathlib import Path
import re
import pandas as pd

import matplotlib.pyplot as plt
from fd_count import (
    get_sizecount,
    plot_determinant_size_area,
    plot_determinant_size_stacked_bar,
    plot_stacked_bar_with_error,
)
from load import load_fds

DATAPATH = "data/"


def main():
    files_to_plot = []

    parser = ArgumentParser()
    parser.add_argument(
        "-s",
        "--data-sources",
        default=files_to_plot,
        nargs="+",
        help="Path to files to plot",
    )
    parser.add_argument("--save", action="store_true", help="If plots should be saved")
    args = parser.parse_args()

    determinant_size_counts = load_and_count(args.data_sources)
    mean, std = calculate_mean_and_errors(determinant_size_counts)
    # plot_determinant_size_area(determinant_size_counts)
    # plot_determinant_size_stacked_bar(determinant_size_counts)
    plot_stacked_bar_with_error(mean, std)

    if args.save:
        out_name = "fd_count_barplot.pdf"
        plt.savefig(out_name)
        print(out_name)
    else:
        plt.show()


def load_and_count(data_sources: list[str]):
    determinant_size_counts = {}
    for idx, data_source in enumerate(data_sources):
        fds = load_fds(data_source)
        data_source_name = Path(data_source).name.rsplit("_", maxsplit=1)[0]
        determinant_size_counts[data_source_name] = get_sizecount(fds)

    return determinant_size_counts

def calculate_mean_and_errors(fd_counts):
    df = pd.DataFrame.from_dict(fd_counts, orient="index")
    df['mode'] = df.index
    df['mode'] =  df['mode'].apply(lambda x: re.sub(r'^\d+_','', str(x)))
    grouped_df = df.groupby("mode")
    mean = grouped_df.mean()
    std = grouped_df.std()
    return (mean, std)


# def load_and_count(data_sources: list[str]):
#     names = []
#     sizecounts = []
#     for idx, data_source in enumerate(data_sources):
#         fds = load_fds(data_source)
#         data_source_name = Path(data_source).name.rsplit("_", maxsplit=1)[0]
#         data_source_name = re.sub('^\d+_', '', data_source_name)
#         names += [data_source_name]
#         sizecounts += [get_sizecount(fds)]

#     return pd.DataFrame.from_dict({"data_source": names, "count": sizecounts})

if __name__ == "__main__":
    main()
