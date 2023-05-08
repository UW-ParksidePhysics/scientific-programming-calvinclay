"""
Finds quadratic coefficients
"""

__author__ = 'Michael Hotchkiss'
import numpy as np


def calculate_quadratic_fit(data):
    """
    This finds quadratic coefficients for a set of data points.
    :param data: ndarray, shape(2,M)
    :return: quadratic_coefficients: ndarray, shape(3,)
    """
    quadratic_coefficients = np.polyfit(data[0], data[1], 2)
    ordered_quadratic_coefficients = [quadratic_coefficients[-1], quadratic_coefficients[1], quadratic_coefficients[0]]

    return ordered_quadratic_coefficients

if __name__ == "__main__":
    value_names = ['constant coefficient' , 'linear coefficient','quadratic coefficient']
    for name, value in zip(value_names,calculate_quadratic_fit([np.linspace(-1, 1), np.linspace(-1,1)**2])):
        print(f'{name}: {value}')
