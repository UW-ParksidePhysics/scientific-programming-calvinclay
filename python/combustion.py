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
Volume_1 = np.pi*(1/2 * 0.0995)**2*(0.079)
Volume_2 = 0.000100
Specific_Heat = 517.15 #244 degrees celcius maybe, have to look at data
# heat of combustion?
Constant_volume = 283.333
Tempature_1= 294
Pressure_0 = 101.3 * 10**3 #atmospheric pressure
k = Pressure_0 * Volume_1**γ
Delta_Tempature = (Specific_Heat/Constant_volume) *1000
Tempature_2 = Tempature_1 + Delta_Tempature
def P(Volume_2):
    return (k / (Volume_2**γ)) + Pressure_0

Pressure_2 = (P(Volume_2)/Tempature_1)*Tempature_2
#Bore of engine = 99.5mm, stroke of engine = 79mm
Volume_Range =np.linspace(Volume_2, Volume_1)
Pressure_Range =P(Volume_Range)

print(Volume_1)
print(P(Volume_2))
print(k)
print(Tempature_2)
print(Pressure_2)

#P_2 to P_3

#V_min to V_max at P_0
pressures = np.full(len(Volume_Range), Pressure_0)
plt.plot(Volume_Range, pressures)

plt.plot(Volume_Range, P(Volume_Range))
plt.xlabel('volume (m**3)')
plt.ylabel('pressure (pascal)')


plt.show()

