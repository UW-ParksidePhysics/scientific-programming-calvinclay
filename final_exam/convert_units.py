from scipy.constants import angstrom, physical_constants


def convert_units(value, units):
    if units == 'cubic bohr/atom':
        new_values = (value * physical_constants['Bohr radis'[0]]/angstrom)**3
    elif units == 'rydberg/atom':
        new_values = value * physical_constants['Rydberg constant times hc in eV']
    elif units == 'rydberg/cubic bohr':
        new_values = value / 29421.02648438959
    else:
        new_values = value
    return new_values
