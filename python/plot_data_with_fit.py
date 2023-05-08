"""
This plots a set of data with a fit curve and the points itself.
"""
__author__ = "Michael and Calvin"

import numpy as np
import matplotlib.pyplot as plt


def plot_data_with_fit(data, fit_curve, data_format="o", fit_format=""):
    """
    This function plots the data with a fit curve and the data itself.
    :param data: ndarray, shape(2,M)
    :param fit_curve: ndarray, shape(2,N)
    :param data_format: str
    :param fit_format: str
    :return: scatter_plot: figure
    :return: curve_plot: figure
    """
    scatter_plot = plt.plot(data[0], data[1], data_format)
    curve_plot = plt.plot(fit_curve[0], fit_curve[1], fit_format)
    return scatter_plot, curve_plot


if __name__ == '__main__':
    data = [[-2, -1, 0, 1, 2], [4, 1, 0, 1, 4]]
    fit_curve = [np.linspace(-2, 2), np.linspace(-2, 2) ** 2]
    plot_data_with_fit(data, fit_curve)
    plt.show()
