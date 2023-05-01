import numpy as np
from scipy import stats




x_values = np.linspace(-10,10,22)
y_values = x_values**2
def calculate_bivariate_statistics(data):
    """
    calculating statistics of the volumes_energies.dat
    :param data:
    :return: statistics: ndarray, shape(6)
    """
    try:
        statistics_x = stats.describe(data[0])
        statistics_y = stats.describe(data[1])
        statistics = np.array([statistics_y.mean, np.sqrt(statistics_y.variance), statistics_x.minmax[0], statistics_x.minmax[1], statistics_y.minmax[0], statistics_y.minmax[1]])
    except IndexError as error:
        print(f'{error}')
    return statistics


if __name__ == "__main__":
    x_values = np.linspace(-10, 10)
    y_values = x_values ** 2
    value_names = ['mean of y', 'std of y', 'min of x', 'max of x', 'min of y', 'max of y']
    expected_values = [np.mean(y_values), np.sqrt(np.var(y_values)), np.min(x_values), np.max(x_values), np.min(y_values), np.max(y_values)]
    for name, expected, value in zip(value_names, expected_values, calculate_bivariate_statistics([x_values,y_values])):
        print(f'{name}: {expected}, {value}')
    #print(calculate_bivariate_statistics(x_values,y_values))

