"""
Read in two columns of data from text file of arbitrary length
"""

__author__ = 'Calvin Clay'

import numpy as np


def read_two_columns_text(filename):
    """
    Read in two columns of data from text file of arbitrary length
    :param filename: str
        Name of the file to be read
    :return: data: ndarray
        Columns of data as rows of array
    """
    try:
        data = np.loadtxt(filename).transpose()
    except OSError as error:
        print(f'{error}')
    return data


if __name__ == "__main__":
    test_file = 'volumes_energies.dat'
    test_data = read_two_columns_text(test_file)
    print(f'{test_data=}, shape={test_data.shape}')
