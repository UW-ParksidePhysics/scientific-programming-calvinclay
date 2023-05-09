from annotate_plot import annotate_plot
from fit_curve_array import fit_curve_array
from plot_data_with_fit import plot_data_with_fit
from read_two_columns_text import read_two_columns_text
from calculate_quadratic_fit import calculate_quadratic_fit
from calculate_bivariate_statistics import calculate_bivariate_statistics
from calculate_lowest_eigenvectors import lowest_eigenvector
from equations_of_state import fit_eos
from generate_matrix import generate_matrix
import matplotlib.pyplot as plt
import numpy as np


def parse_file_name(filename):
    parse = filename.split(".")
    chemical_symbol = parse[0]
    crystal_symbol = parse[1]
    acronym = parse[2]
    return chemical_symbol, crystal_symbol, acronym


filename = 'C.Fd-3m.GGA-PBE.volumes_energies.dat'
chemical_symbol, crystal_symbol, acronym = parse_file_name(filename)
array = read_two_columns_text(filename)
statistics = calculate_bivariate_statistics(array)
min_x = statistics[2]
max_x = statistics[3]
min_y = statistics[4]
max_y = statistics[5]

quadratic_coefficients = calculate_quadratic_fit(array)
eos_fit_curve, eos_parameters = fit_eos(array[0], array[1], quadratic_coefficients)

array_2 = fit_curve_array(quadratic_coefficients, min_x, max_x, number_of_points=100)

annotations_chemical = {'string': chemical_symbol, 'position': np.array([62.30, -36.84670]),
               'alignment': ['left', 'top'], 'fontsize': 10}
annotations_crystal = {'string': crystal_symbol,
               'position': np.array([(max_x * 1.1 - min_x / 1.1) / 2 + min_x / 1.1, -36.84664]),
               'alignment': ['center', 'top'], 'fontsize': 10}
annotations_bulk = {'string': crystal_symbol,
               'position': np.array([(max_x * 1.1 - min_x / 1.1) / 2 + min_x / 1.1, max_y-.0001]),
               'alignment': ['center', 'top'], 'fontsize': 10}

plt.figure(figsize=(15,8))
plt.title(f'(Murnaghan) Equation of State for {chemical_symbol} in DFT {acronym}')
plot = plot_data_with_fit(array, array_2, data_format="o", fit_format="")
plt.xlim(min_x / 1.1, max_x * 1.1)
plt.ylim(min_y * 1.00005, max_y / 1.00005)
plt.xlabel('$\mathit{E}$ $\mathrm{ev/atom}$')
plt.ylabel('$\mathit{V}$ $\mathrm{\AA/atom}$')
annotate_plot(annotations_chemical)
annotate_plot(annotations_crystal)
annotate_plot(annotations_bulk)

plt.show()

################
potential = 'square'
Ndim = 90
parameter = 100
matrix = generate_matrix(min_x, max_x, Ndim, potential, parameter)