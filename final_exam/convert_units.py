from scipy.constants import angstrom, physical_constants


def convert_units(value, units):
    if units == 'cubic bohr/atom':
        new_values = value * physical_constants['Bohr radius'][0]**3/angstrom**3
    elif units == 'rydberg/atom':
        new_values = value * physical_constants['Rydberg constant times hc in eV'][0]
    elif units == 'rydberg/cubic bohr':
        new_values = value * physical_constants['Rydberg constant times hc in J'][0]/\
            physical_constants['Bohr radius'][0]
    else:
        new_values = value
    return new_values
