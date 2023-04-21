import numpy as np
from math import pi
from matplotlib import pyplot as plt, pyplot


def scrape_web_data(url):
    import pandas as pd

    url_data = pd.read_html(url)
    return url_data


if __name__ == '__main__':
    gas_data_url = 'https://www.ohio.edu/mechanical/thermo/property_tables/gas/idealGas.html'
    gas_data = scrape_web_data(gas_data_url)[0]
    gas_names = gas_data[0]
    gas_ratios = gas_data[6]
    desired_gases = ['Hydrogen', 'Methane', 'Octane', 'Butane']
    gas_ratios_dictionary = {}
    for desired_gas in desired_gases:
        for index, row in gas_data.iterrows():
            if row[0] == desired_gas:
                gas_ratios_dictionary[row[0]] = row[6]

    gas_data = scrape_web_data(gas_data_url)[0]
    gas_names = gas_data[0]
    gas_ratios = gas_data[6]
    desired_gases = ['Hydrogen', 'Methane', 'Octane', 'Butane']
    gas_data_dictionary = {}
    for desired_gas in desired_gases:
        for index, row in gas_data.iterrows():
            if row[0] == desired_gas:
                gas_data_dictionary[row[0]] = {
                    'isochoric specific heat': row[5],
                    'specific heat ratio': row[6]
                }

    combustion_data_url = 'https://en.wikipedia.org/wiki/Heat_of_combustion'
    combustion_data = scrape_web_data(combustion_data_url)[3]
    for desired_gas in desired_gases:
        for index, row in combustion_data.iterrows():
            if row[0] == desired_gas:
                gas_data_dictionary[row[0]]['heat of combustion'] = row[4]

    print(gas_data_dictionary)

    # volume range to plot over -- use np.linspace()
    # define P(V) = k / V^γ + P_0
    # calculate ΔT at fixed V
    # define P2
# Hydrogen
γ = 1.405
open_volume = np.pi * (1 / 2 * 0.0995) ** 2 * (0.079)
compressed_volume = 0.000100
isobaric_heat_capacity = 517.15  # 244 degrees celsius maybe, have to look at data
# heat of combustion?
isochoric_heat_capacity = 283.333
initial_temperature = 294
initial_pressure = 101.3 * 10 ** 3  # atmospheric pressure
adiabatic_constant_1_2 = initial_pressure * open_volume ** γ
temperature_change = (isobaric_heat_capacity / isochoric_heat_capacity) * 1000
raised_temperature = initial_temperature + temperature_change


def calculate_pressure(volume, k, initial_pressure):
    return (k / (volume ** γ)) + initial_pressure


adiabatic_raised_pressure = calculate_pressure(compressed_volume, adiabatic_constant_1_2, initial_pressure)
adiabatic_constant_3_4 = adiabatic_raised_pressure * open_volume ** γ
adiabatic_lowered_pressure = calculate_pressure(open_volume, adiabatic_constant_3_4, adiabatic_raised_pressure)
isochoric_raised_pressure = (adiabatic_raised_pressure / initial_temperature) * raised_temperature
# Bore of engine = 99.5mm, stroke of engine = 79mm
volume_range = np.linspace(compressed_volume, open_volume)
volumes = [volume_range,  # 0->1; [V_min, V_max]
           volume_range,  # 1->2; [V_min, V_max]
           np.full(len(volume_range), compressed_volume),  # 2->3; [V_min, V_min]
           volume_range,  # 3->4; [V_max, V_min]
           np.full(len(volume_range), open_volume)  # 4->5; [V_max, V_max]
           ]

# Pressure_Range = calculate_pressure(volume_range, adiabatic_constant_1_2, initial_pressure)

# print(open_volume)
# print(P(compressed_volume))
# print(raised_temperature)
# print(isochoric_raised_pressure)


# P_2 to P_3
# V_min to V_max at P_0

pressures = [np.full(len(volume_range), initial_pressure),                                              # P = P_0
             calculate_pressure(volume_range, adiabatic_constant_1_2, initial_pressure),                # P = k_12 / V^γ
             np.linspace(adiabatic_raised_pressure, isochoric_raised_pressure, num=len(volume_range)),  # P = P2 (T2/T1)
             calculate_pressure(volume_range, adiabatic_constant_3_4, adiabatic_raised_pressure),        # P = k_34 / V^γ
             np.linspace(adiabatic_lowered_pressure, initial_pressure, num=len(volume_range))
             ]
for volume, pressure in zip(volumes, pressures):
    plt.plot(volume, pressure)

# pressures_1 = np.full(len(Pressure_Range), Volume_2)
# plt.plot(Pressure_Range, pressures_1)

# plt.plot(Volume_Range, P(Volume_Range, adiabatic_constant_1_2, compressed_volume))
# plt.xlabel('volume (m**3)')
# plt.ylabel('pressure (pascal)')


# plt.plot(np.full(len(compressed_volume, )


plt.show()
