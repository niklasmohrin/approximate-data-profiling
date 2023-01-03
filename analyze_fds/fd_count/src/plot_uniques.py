from argparse import ArgumentParser
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def main():
    parser = ArgumentParser()
    parser.add_argument(
        "-s",
        "--data-source",
        help="Path to unique value csv",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.data_source)
    print("Read csv")

    # df.plot(kind="bar", x="method", y="uniques_determinant")
    # print("Plot done")
    # breakpoint()
    methods = df["method"].unique()
    offset = 0.01
    min_x = df["uniques_dependant"].min() - offset
    max_x = df["uniques_dependant"].max() + offset
    min_y = df["uniques_determinant"].min() - offset
    max_y = df["uniques_determinant"].max() + offset
    for m in methods:
        target = df.where(df["method"] == m)
        max_error = target["error"].max()
        cinterval = [0, 0.1] if max_error == 0 else None
        target.plot.hexbin(
            x="uniques_dependant",
            y="uniques_determinant",
            C="error",
            title="Correlation of Error to uniques in determinants and dependant",
            xlim=[min_x, max_x],
            ylim=[min_y, max_y],
            clim=cinterval,
            cmap="plasma"
        )
        plt.suptitle(m)
        plt.tight_layout()

        out_path = Path(args.data_source).with_name(f"uniqueness_error_{m}.pdf")
        plt.savefig(out_path)

        # sns.barplot(df, x="method", y="uniques_determinant")
        # plt.show()


if __name__ == "__main__":
    main()
