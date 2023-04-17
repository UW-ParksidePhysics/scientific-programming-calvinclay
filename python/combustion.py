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
k = 1.405
γ= k
V_1 = pi*(1/2 * 99.5)**2*(79)
V_2 = 0.100
P_0= 14.7
#atmospheric pressure
T_2= 244
# heat of combustion?
T_1= 25
def P(V_2): #psi
    return k / V_2**γ + P_0

#Bore of engine = 99.5mm, stroke of engine = 79mm
Volume_Range =np.linspace(V_2, V_1)
Pressure_Range =np.linspace(P(V_2), P_0)
print(V_1)
print(P(V_2))


plt.plot(Volume_Range, Pressure_Range)
plt.xlabel('volume (mm**3)')
plt.ylabel('pressure (psi)')
plt.plot(P_0)
plt.show()
