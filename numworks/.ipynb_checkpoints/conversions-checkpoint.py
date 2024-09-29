'''conversion functions
''' 

from math import (sqrt)

BOLTZMAN = 1.38065e-23

def celsius_to_kelvin(temp_celsius):
    '''celsius to kelvin'''
    return 273.15 + temp_celsius

def resistor_vrms(temp_kelvin, resistance, bandwidth):
    '''resistor rms thermal noise'''
    return sqrt((4 * BOLTZMAN)*temp_kelvin*resistance*bandwidth)

def vrms_to_vpp(vrms):
    '''rms to pp'''
    return 6.6 * vrms
