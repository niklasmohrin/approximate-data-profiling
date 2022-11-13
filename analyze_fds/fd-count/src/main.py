from argparse import ArgumentParser
import matplotlib.pyplot as plt

from load import load_fds
from fd_count import get_sizecount, plot_determinant_size_area, plot_determinant_size_stacked_bar


DATAPATH = 'data/';

def main():
    files_to_plot = ['full', 'random_10', 'kmeans_10']

    parser = ArgumentParser()
    parser.add_argument('-s', '--data-sources', default=files_to_plot, nargs='+', help='List of names of data sources (without json)')
    parser.add_argument('-p', '--data-path', default=DATAPATH, help='Path to folder of data')
    args = parser.parse_args()

    determinant_size_counts = {}
    for idx, data_source in enumerate(args.data_sources):
        fds = load_fds(args.data_path, data_source)
        determinant_size_counts[data_source] = get_sizecount(fds)

    plot_determinant_size_area(determinant_size_counts)
    plot_determinant_size_stacked_bar(determinant_size_counts)

    plt.show()

if __name__ == '__main__':
    main()