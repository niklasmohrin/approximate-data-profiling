from argparse import ArgumentParser

import matplotlib.pyplot as plt
from fd_count import (
    get_sizecount,
    plot_determinant_size_area,
    plot_determinant_size_stacked_bar,
)
from load import load_fds
from pathlib import Path

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

    plot_determinant_size_area(determinant_size_counts)
    plot_determinant_size_stacked_bar(determinant_size_counts)

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
        data_source_name = Path(data_source).name.split('_', maxsplit=2)[-1]
        determinant_size_counts[data_source_name] = get_sizecount(fds)

    return determinant_size_counts


if __name__ == "__main__":
    main()
