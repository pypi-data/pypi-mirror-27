# -*- coding: utf-8 -*-
#
from .helpers import mu0

magnetic_permeability = mu0
electrical_conductivity = 0.0

# http://www.engineeringtoolbox.com/argon-d_1414.html
specific_heat_capacity = 523.0
thermal_conductivity = 0.0172


def density(T):
    '''https://en.wikipedia.org/wiki/Argon tells us that for 0°C, 101.325
    kPa, the density is 1.784 kg/m^3.  Assuming then that only density and
    temperature change, the ideal gas law :math:`PV = nRT` gives us the
    complete formula.
    '''
    return 1.784 * 273.15 / T
