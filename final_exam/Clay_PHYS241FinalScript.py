"""
The following code takes the data from volume_energies.dat, converts units, then plots based off the Murnaghan
Equation of State. Finally, the Sinusoidal Wave is plotted with the first 3 matrices following data.

"""
from annotate_plot import annotate_plot
from plot_data_with_fit import plot_data_with_fit
from read_two_columns_text import read_two_columns_text
from calculate_quadratic_fit import calculate_quadratic_fit
from calculate_bivariate_statistics import calculate_bivariate_statistics
from calculate_lowest_eigenvectors import lowest_eigenvector
from equations_of_state import fit_eos
from generate_matrix import generate_matrix
import matplotlib.pyplot as plt
import numpy as np
from datetime import date
from convert_units import convert_units


def parse_file_name(file):
    """
    Give the file name 'C.Fd-3m.GGA-PBE.volumes_energy.dat' to the function to split into 3 strings.
    :param file: C.Fd-3m.GGA-PBE.volumes_energy.dat
    :return: str, parse[0]
    :return: str, parse[1]
    :return: str, parse[3]
    """
    parse = file.split(".")
    return parse[0], parse[1], parse[2]


if __name__ == '__main__':
    display_graph = True
    filename = 'C.Fd-3m.GGA-PBE.volumes_energies.dat'
    chemical_symbol, crystal_symbol, acronym = parse_file_name(filename)
    array = (read_two_columns_text(filename)) / 2

    quad_coefficients_temp = calculate_quadratic_fit(array)
    quadratic_coefficients = quad_coefficients_temp[::-1]

    eos_fit_curve, eos_parameters = fit_eos(array[0], array[1], quadratic_coefficients, eos='murnaghan')

    converted_units = [convert_units(eos_parameters[0], 'rydberg/atom'),
                       convert_units(eos_parameters[1], 'rydberg/cubic bohr'),
                       eos_parameters[2], convert_units(eos_parameters[3], 'cubic bohr/atom')
                       ]

    data_array = np.array([convert_units(array[0], 'cubic bohr/atom'),
                           convert_units(array[1], 'rydberg/atom')])

    statistics = calculate_bivariate_statistics(data_array)
    min_x = statistics[2]
    max_x = statistics[3]
    min_y = statistics[4]
    max_y = statistics[5]

    fit_array = np.array([np.linspace(min_x, max_x, len(eos_fit_curve)),
                          convert_units(eos_fit_curve, 'rydberg/atom')])
    plot_miny = min(fit_array[1])
    plot_minx = min(fit_array[0])
    plot_maxy = max(fit_array[1])
    plot_maxx = max(fit_array[0])

    annotations_chemical = {'string': f"{chemical_symbol}",
                            'position': np.array([min_x - 0.3 * (max_x - min_x), max_y - .00005]),
                            'alignment': ['left', 'center'], 'fontsize': 10}

    annotations_crystal = {
        'string': rf"${crystal_symbol[:2]}" + r"\overline{" + crystal_symbol[-2] + r"}" + crystal_symbol[-1] + r" $",
        'position': np.array([(max_x * 1.1 - min_x / 1.1) / 2 + min_x / 1.1, max_y - 0.005]),
        'alignment': ['center', 'center'], 'fontsize': 10}

    annotations_bulk = {'string': rf'$K_0= ${converted_units[1]:.1f} GPa',
                        'position': np.array([(max_x * 1.1 - min_x / 1.1) / 2 + min_x / 1.1, max_y]),
                        'alignment': ['center', 'center'], 'fontsize': 10}

    annotations_V0 = {'string': rf'$V_0$ = {converted_units[3]:.2f} $\AA^3/$atom',
                      'position': np.array([converted_units[3] + (max_x - min_x) * .05, max_y - .14]),
                      'alignment': ['left', 'bottom'], 'fontsize': 10}

    name = 'Calvin Clay'
    annotations_sign = {'string': f"Created by {name} {date.today().isoformat()}",
                        'position': np.array([min_x - 0.3 * (max_x - min_x), min_y - 0.004]),
                        'alignment': ['left', 'bottom'],
                        'fontsize': 10}

    plt.figure(figsize=(10, 6))

    plot = (plot_data_with_fit(data_array, fit_array, data_format="o", fit_format=""))
    plt.xlim(min_x / 1.1, max_x * 1.1)
    plt.plot(np.linspace(converted_units[3], converted_units[3], 50),
             np.linspace(np.amin(fit_array[1]), (np.amin(fit_array[1]) + min_y * 1.00005 / 2)), 'k--')
    plt.ylim(min_y * 1.00002, max_y / 1.00002)
    plt.ylabel(r'$E$' + ' ' + r"[eV/atom]")
    plt.xlabel(r'$V$' + ' ' + r"[$\AA^3/$atom]")
    annotate_plot(annotations_chemical)
    annotate_plot(annotations_V0)
    annotate_plot(annotations_crystal)
    annotate_plot(annotations_bulk)
    annotate_plot(annotations_sign)
    plt.title(f'Murnaghan Equation of State for {chemical_symbol} in DFT {acronym}')
    if display_graph == 'True':
        plt.show()
    else:
        plt.savefig('Murnaghan.png')

    ##########
    number_of_eigenvalues = 3
    matrix = generate_matrix(-10, 10, 90, 'Square', 100)
    eigenvalue, eigenvector = lowest_eigenvector(matrix, number_of_eigenvalues)
    eigenvalues = eigenvalue[:number_of_eigenvalues]
    eigenvectors = eigenvector[:number_of_eigenvalues]
    x = np.linspace(-10, 10, 90)
    labels = []
    for i in range(number_of_eigenvalues):
        labels.append(rf'$\psi_' + r'{' + rf'{i}' + r'},' + rf'E_{i} $ = {eigenvalue[i]:.3f}a.u.')
    plt.figure(figsize=(12, 8))
    for eigenvector in eigenvectors:
        plt.plot(x, eigenvector)
    plt.xlabel(r'$x$ [a.u.]')
    plt.ylabel(r'$\psi_n (x)$ [a.u.]')
    plt.legend(labels=labels, loc='upper right')
    plt.ylim(-2 * np.amax(eigenvectors), 2 * np.amax(eigenvectors))
    plt.plot(x, np.linspace(0, 0, 90), color='black')
    plt.title(f"Select Wavefuctions for a {'Square'} Potential\n"
              f"on a Spatial Grid of 90 Points")
    name = 'Calvin Clay'
    plt.annotate(f'Created by {name} {date.today().isoformat()}', (.02, .054), (-7.5, .25),
                 xycoords='axes fraction', textcoords='offset points', va='top')

    if display_graph:
        plt.show()
    else:
        plt.savefig('Square.png')
