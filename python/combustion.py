import numpy as np
from math import pi
from matplotlib import pyplot as plt, pyplot


def scrape_web_data(url):
    import pandas as pd

    url_data = pd.read_html(url)
    return url_data


def get_gas_data():
    gas_data_url = 'https://www.ohio.edu/mechanical/thermo/property_tables/gas/idealGas.html'
    gas_data = scrape_web_data(gas_data_url)[0]
    # gas_names = gas_data[0]
    # gas_ratios = gas_data[6]
    desired_gases = ['Hydrogen', 'Methane', 'Octane', 'Butane']
    # gas_ratios_dictionary = {}
    # for desired_gas in desired_gases:
    #     for index, row in gas_data.iterrows():
    #         if row[0] == desired_gas:
    #             gas_ratios_dictionary[row[0]] = row[6]

    # gas_data = scrape_web_data(gas_data_url)[0]
    # gas_names = gas_data[0]
    # gas_ratios = gas_data[6]
    # desired_gases = ['Hydrogen', 'Methane', 'Octane', 'Butane']
    gas_data_dictionary = {}
    for desired_gas in desired_gases:
        for index, row in gas_data.iterrows():
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
    for gas, density in zip(desired_gases, fuel_densities):
        gas_data_dictionary[gas]['density'] = density
    return gas_data_dictionary


def extract_gas_data(gas_name, data_dictionary):
    return data_dictionary[gas_name]['density'], data_dictionary[gas_name]['specific heat ratio'], \
        data_dictionary[gas_name]['isochoric specific heat'], data_dictionary[gas_name]['heat of combustion']


def calculate_pressure(input_volume, k, exponent):
    return k / np.power(input_volume, exponent)


def calculate_otto_cycle_pressures(volumes, parameters):
    gamma = parameters[0]
    initial_pressure = parameters[1]
    heat_of_combustion = parameters[2]
    isochoric_specific_heat = parameters[3]
    initial_temperature = parameters[4]
    fuel_mass = parameters[5]
    compressed_volume = volumes[0][0]
    open_volume = volumes[0][-1]

    density_of_air = 1.205 #kg/m**3
    air_mass = density_of_air*open_volume
    air_isochoric_specific_heat = 718

    adiabatic_constant_1_2 = initial_pressure * open_volume ** gamma
    temperature_change = (fuel_mass*heat_of_combustion) / (air_mass*air_isochoric_specific_heat)
    raised_temperature = initial_temperature + temperature_change
    print(f'T={temperature_change}')
    print(f'Fuel={fuel_mass}')
    print(f'Air mass={air_mass}')
    print(f'heat of combustion= {heat_of_combustion}')
    print(f'air of specific heat= {air_isochoric_specific_heat}')

    adiabatic_raised_pressure = calculate_pressure(compressed_volume, adiabatic_constant_1_2, gamma)
    isochoric_raised_pressure = adiabatic_raised_pressure * (raised_temperature / initial_temperature)
    adiabatic_constant_3_4 = isochoric_raised_pressure * compressed_volume ** gamma
    adiabatic_lowered_pressure = calculate_pressure(open_volume, adiabatic_constant_3_4, gamma)
    print(f'k_12, k_34 = {adiabatic_constant_1_2}, {adiabatic_constant_3_4}')
    print(f'p_1, p_2, p_3, p_4 = {initial_pressure}, {adiabatic_raised_pressure}, {isochoric_raised_pressure}, {adiabatic_lowered_pressure}')

    pressures = [np.full(len(volumes[0]), initial_pressure),  # P = P_0
                 calculate_pressure(volumes[0], adiabatic_constant_1_2, initial_pressure),  # P = k_12 / V^γ
                 np.linspace(adiabatic_raised_pressure, isochoric_raised_pressure, num=len(volumes[0])),
                 # P = P2 (T2/T1)
                 calculate_pressure(volumes[0], adiabatic_constant_3_4, isochoric_raised_pressure),  # P = k_34 / V^γ
                 np.linspace(adiabatic_lowered_pressure, initial_pressure, num=len(volumes[0]))
                 ]
    return pressures


if __name__ == '__main__':
    gas_data = get_gas_data()
    print(gas_data)

    # Bore of engine = 99.5mm, stroke of engine = 79mm
    open_volume = np.pi * (1 / 2 * 0.0995) ** 2 * (0.079)
    compressed_volume = 0.000100
    # volumes for Otto Cycle
    volume_range = np.linspace(compressed_volume, open_volume)
    volumes = [volume_range,  # 0->1; [V_min, V_max]
               volume_range,  # 1->2; [V_min, V_max]
               np.full(len(volume_range), compressed_volume),  # 2->3; [V_min, V_min]
               volume_range,  # 3->4; [V_max, V_min]
               np.full(len(volume_range), open_volume)  # 4->5; [V_max, V_max]
               ]
    print(f'open volume{open_volume}')
    # initial conditions
    fuel_to_air_ratio = 1 / 14.7
    initial_temperature = 294
    initial_pressure = 101.3 * 10 ** 3  # atmospheric pressure
    density_of_air = 1.205 #kg/m**3
    air_mass = density_of_air*open_volume
    air_specific_heat = 0.718

    figure, axes = plt.subplots(ncols=2, nrows=3)
    column_index, row_index = 0, 0
    #for index, gas in enumerate(gas_data.keys()):
    gas='Hydrogen'
    index=0
    fuel_density, γ, isochoric_specific_heat, heat_of_combustion = extract_gas_data(gas, gas_data)
    fuel_mass = fuel_to_air_ratio * open_volume * fuel_density
    gas_pressures = calculate_otto_cycle_pressures(volumes, [γ, initial_pressure, heat_of_combustion,
                                                             isochoric_specific_heat,
                                                             initial_temperature, fuel_mass])
    heat_in = fuel_mass * heat_of_combustion
    column_index, row_index = index % 2, int(index / 2)
    for branch_index, (volume, pressure) in enumerate(zip(volumes, gas_pressures)):
        axes[column_index][row_index].plot(volume, pressure, label=f"{branch_index}")
        # axes[column_index][row_index].legend()

# efficency
# net_work = np.trapz(pressures[3], volume_range) - np.trapz(pressures[1], volume_range)
# efficency = net_work / heat_in
# print(efficency)
plt.show()
