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
#Hydrogen
γ = 1.405
open_volume = np.pi * (1 / 2 * 0.0995) ** 2 * (0.079)
compressed_volume = 0.000100
Specific_Heat = 517.15 #244 degrees celcius maybe, have to look at data
# heat of combustion?
Constant_volume = 283.333
Tempature_1= 294
Pressure_0 = 101.3 * 10**3 #atmospheric pressure
adiabatic_constant_1_2 = Pressure_0 * open_volume ** γ
Delta_Tempature = (Specific_Heat/Constant_volume) *1000
Tempature_2 = Tempature_1 + Delta_Tempature
def P(volume, k, initial_pressure):
    return (k / (volume**γ)) + initial_pressure

Pressure_2 = (P(compressed_volume, adiabatic_constant_1_2, Pressure_0) / Tempature_1) * Tempature_2
#Bore of engine = 99.5mm, stroke of engine = 79mm
Volume_Range =np.linspace(compressed_volume, open_volume)
volumes = [Volume_Range, Volume_Range, np.full(len(Volume_Range), compressed_volume), compressed_volume, Volume_Range,
           np.full(len(Volume_Range), compressed_volume), (open_volume)]
Pressure_Range =P(Volume_Range, adiabatic_constant_1_2, Pressure_0)


print(open_volume)
#print(P(compressed_volume))

print(Tempature_2)
print(Pressure_2)

#P_2 to P_3

#V_min to V_max at P_0

pressures = [np.full(len(Volume_Range), Pressure_0), P(Volume_Range, adiabatic_constant_1_2, Pressure_0),
             np.linspace(P(Pressure_2, adiabatic_constant_1_2, Pressure_0), num=len(Volume_Range), stop=True)]
for pressure in pressures:
    plt.plot(Volume_Range, pressure)

#pressures_1 = np.full(len(Pressure_Range), Volume_2)
#plt.plot(Pressure_Range, pressures_1)

plt.plot(Volume_Range, P(Volume_Range, adiabatic_constant_1_2, compressed_volume))
plt.xlabel('volume (m**3)')
plt.ylabel('pressure (pascal)')


#plt.plot(np.full(len(compressed_volume, )


plt.show()

