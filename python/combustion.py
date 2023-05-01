import numpy as np
from matplotlib import pyplot as plt, pyplot


def scrape_web_data(url):
    """
    Script the url to find data
    :param url: URL for page with data to find
    :return: url_data
    """
    import pandas as pd

    url_data = pd.read_html(url)
    return url_data


def get_gas_data():
    """
    Define gas data and pick the gases that we want to use.
    Then we make gas dictionary that has gas name as keys and particular properties as the values
    :return: gas_data_dictionary {'gas': isochoric specific heat, specific heat ratio, heat of combustion, density}
    """
    gas_data_url = 'https://www.ohio.edu/mechanical/thermo/property_tables/gas/idealGas.html'
    webiste_gas_data = scrape_web_data(gas_data_url)[0]
    desired_gases = ['Hydrogen', 'Methane', 'Octane', 'Butane']
    gas_data_dictionary = {}
    for desired_gas in desired_gases:
        for index, row in webiste_gas_data.iterrows():
            if row[0] == desired_gas:
                gas_data_dictionary[row[0]] = {
                    'isochoric specific heat': float(row[5]) * 1e3,
                    'specific heat ratio': float(row[6])
                }

    combustion_data_url = 'https://en.wikipedia.org/wiki/Heat_of_combustion'
    combustion_data = scrape_web_data(combustion_data_url)[0]
    for desired_gas in desired_gases:
        for index, row in combustion_data.iterrows():
            if row[0] == desired_gas:
                gas_data_dictionary[row[0]]['heat of combustion'] = row[1] * 1e6
    gas_data_dictionary['Octane']['heat of combustion'] = 4.792e7
    fuel_densities = [0.08988, 0.6682, 702.3, 2.496]
    for particular_gas, density in zip(desired_gases, fuel_densities):
        gas_data_dictionary[particular_gas]['density'] = density
    return gas_data_dictionary


def extract_gas_data(gas_name, data_dictionary):
    """
    Extracts density, specific heat ratio, isochoric specific heat, heat of combustion of the gas_name from
    data_dictionary.
    :param gas_name:
    :param data_dictionary:
    :return density, specific_heat_ratio, isochoric_specific_heat, heat_of_combustion:
    """
    return data_dictionary[gas_name]['density'], data_dictionary[gas_name]['specific heat ratio'], \
           data_dictionary[gas_name]['isochoric specific heat'], data_dictionary[gas_name]['heat of combustion']


def calculate_pressure(input_volume, k, exponent):
    """
    Pressure equation
    :param input_volume: array of volume of a certain gas
    :param k: constant
    :param exponent: specific heat ratio of a certain gas
    :return pressure: P = k/V^γ
    """
    return k / np.power(input_volume, exponent)


def calculate_otto_cycle_pressures(volume_array, parameters):
    """
    A function of the compressible volumes as the otto cycle is in process.
    :param volume_array:
    :param parameters:
    :return: pressures
    """
    gamma = parameters[0]
    starting_pressure = parameters[1]
    combustion_heat = parameters[2]
    # isochoric_specific_heat = parameters[3]
    starting_temperature = parameters[4]
    combustible_mass = parameters[5]
    smaller_volume = volume_array[0][0]
    larger_volume = volume_array[0][-1]

    air_density = 1.205  # kg/m**3
    piston_air_mass = air_density * larger_volume
    air_isochoric_specific_heat = 718  # J / (kg K)

    # Temperature calculations
    temperature_change = (combustible_mass * combustion_heat) / (piston_air_mass * air_isochoric_specific_heat)
    raised_temperature = starting_temperature + temperature_change

    # Calculating curves of pressures on volume
    adiabatic_constant_1_2 = starting_pressure * larger_volume ** gamma  # Const. for 1 to 2 curve
    adiabatic_raised_pressure = calculate_pressure(smaller_volume, adiabatic_constant_1_2,
                                                   gamma)  # Pressure increase that increases heat
    isochoric_raised_pressure = adiabatic_raised_pressure * (
            raised_temperature / starting_temperature)  # increase in pressure due to increase in heat of cylinder
    adiabatic_constant_3_4 = isochoric_raised_pressure * smaller_volume ** gamma  # Const. for 3 to 4 curve
    adiabatic_lowered_pressure = calculate_pressure(larger_volume, adiabatic_constant_3_4,
                                                    gamma)  # Pressure decrease that decreases heat

    # Graphing pressures
    pressures = [np.full(len(volume_array[0]), starting_pressure),  # P = P_0
                 calculate_pressure(volume_array[0], adiabatic_constant_1_2, gamma),  # P = k_12 / V^γ
                 np.linspace(adiabatic_raised_pressure, isochoric_raised_pressure, num=len(volume_array[0])),
                 # P = P2 (T2/T1)
                 calculate_pressure(volume_array[0], adiabatic_constant_3_4, gamma),  # P = k_34 / V^γ
                 np.linspace(adiabatic_lowered_pressure, starting_pressure, num=len(volume_array[0]))
                 ]
    return pressures


def plot_gas_data(initial_conditions, particular_gas_data):
    """
    Plot the Otto cycle P-V diagram for each gas
    :param particular_gas_data:
    :param initial_conditions:
    :return:
    """
    pressure_1 = initial_conditions[0]
    temperature_1 = initial_conditions[1]
    all_gas_pressures = {}
    index, column_index, row_index = 0, 0, 0
    for gas in particular_gas_data.keys():
        fuel_density, γ, isochoric_specific_heat, heat_of_combustion = extract_gas_data(gas, particular_gas_data)
        fuel_mass = fuel_to_air_ratio * open_volume * fuel_density
        gas_pressures = calculate_otto_cycle_pressures(volumes, [γ, pressure_1, heat_of_combustion,
                                                                 isochoric_specific_heat,
                                                                 temperature_1, fuel_mass])
        all_gas_pressures[gas] = gas_pressures
        column_index, row_index = index % 2, int(index / 2)
        index += 1

        for branch_index, (volume, pressure) in enumerate(zip(volumes, gas_pressures)):
            axes[column_index][row_index].plot(volume, pressure, label=f"{branch_index}")
        axes[column_index][row_index].set_title(gas)
    return all_gas_pressures


def calculate_work(given_volumes, given_pressures, given_gas_data):
    """
    Calculate the heat in and the net work done by the cycle for each gas in the given data
    :param given_volumes:
    :param given_pressures:
    :param given_gas_data:
    :return:
    """
    given_volume_range=given_volumes[0]
    for given_gas in given_gas_data:
        fuel_density, _, _, heat_of_combustion = extract_gas_data(given_gas, given_gas_data)
        given_gas_data[given_gas]['heat in'] = fuel_density * heat_of_combustion
        net_work = np.trapz(given_pressures[given_gas][3], given_volume_range) - np.trapz(given_pressures[given_gas][1], given_volume_range)
        given_gas_data[given_gas]['net work'] = net_work
    return given_gas_data


def plot_efficiency(expanded_gas_data):
    """
    Plots work out vs work in for all the works given in works_to_plot
    :param works_to_plot:
    :return:
    """
    for worked_gas in expanded_gas_data.keys():
        plt.scatter(expanded_gas_data[worked_gas]['heat in'],
                    expanded_gas_data[worked_gas]['net work'],
                    label=worked_gas)
    # efficiency = net_work / heat_in
    plt.xlabel('heat in')
    plt.ylabel('net work')
    plt.yscale('log')
    plt.legend()
    return


if __name__ == '__main__':
    gas_data = get_gas_data()

    # Define volumes set by piston dimensions
    #       bore of engine = 99.5mm, stroke of engine = 79mm
    open_volume = np.pi * (1 / 2 * 0.0995) ** 2 * 0.079
    compressed_volume = 0.000100

    # Create volume range for Otto cycle
    volume_range = np.linspace(compressed_volume, open_volume)
    volumes = [volume_range,  # 0->1; [V_min, V_max]
               volume_range,  # 1->2; [V_min, V_max]
               np.full(len(volume_range), compressed_volume),  # 2->3; [V_min, V_min]
               volume_range,  # 3->4; [V_max, V_min]
               np.full(len(volume_range), open_volume)  # 4->5; [V_max, V_max]
               ]

    # Set initial conditions
    fuel_to_air_ratio = 1 / 14.7
    initial_temperature = 294
    initial_pressure = 101.3 * 10 ** 3  # atmospheric pressure
    density_of_air = 1.205  # kg/m**3
    air_mass = density_of_air * open_volume
    air_specific_heat = 0.718

    # Plot data
    figure, axes = plt.subplots(ncols=2, nrows=2)
    calculated_pressures = plot_gas_data([initial_pressure, initial_temperature], gas_data)
    calculated_works = calculate_work(volumes, calculated_pressures, gas_data)

    plt.show()
    plot_efficiency(calculated_works)
    plt.show()
