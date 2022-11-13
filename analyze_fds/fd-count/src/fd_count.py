'''
Utilities to plot the number of FDs of a specific size
'''
from itertools import chain
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd


def plot_determinant_size_area(fd_counts: dict[str, list[int]]):
    df = pd.DataFrame.from_dict(fd_counts, orient='index')

    df.transpose().plot.area()

    # Set labels and legend
    plt.gca().legend(title='Data Source')
    plt.gca().set_xlabel('Relative number of FDs')
    plt.gca().set_ylabel(f'Size of Determinant')
    plt.gca().set_title('Number of FDs per Determinant Size')

def plot_determinant_size_stacked_bar(fd_counts: dict[str, list[int]], *, normalize_fdcount=False):
    df = pd.DataFrame.from_dict(fd_counts, orient='index')
    if normalize_fdcount:
        df = df.div(df.sum(axis=1), axis=0)

    df.transpose().plot(kind='barh', rot=0, logx=(not normalize_fdcount))
    if normalize_fdcount:
        # Set Percentage as xaxis formatter, with values between 0-1
        plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))

    # Set labels and legend
    plt.gca().legend(title='Data Source')
    plt.gca().set_ylabel('Relative number of FDs')
    plt.gca().set_xlabel(f'Size of Determinant ({"abs, normalized" if normalize_fdcount else "log"})')
    plt.gca().set_title('Number of FDs per Determinant Size')


def get_sizecount(fds: dict[str, list[str]]) -> list[int]:
    '''
    Returns a list of counts for fds where the size of the determinant is index
    '''

    determinants_flat = list(chain.from_iterable([fds[k] for k in fds.keys()]))
    lengths = list(map(lambda l: len(l), determinants_flat))
    
    determinant_size_count = np.bincount(lengths)
    return determinant_size_count


# TODO: not needed?
def find_different_length(trueFd: dict[str, list], b: dict[str, list]):
    # Assume keys are identical
    for k, true_v in trueFd.items():
        b_v = b[k]

        if len(true_v) == len(b_v) and len(true_v) != 0:
            print('# Correct FD: ')
            print(f'# Dependent')
            print(k)
            print(f'# Determinants ({len(true_v)} pairs)')
            print(true_v)