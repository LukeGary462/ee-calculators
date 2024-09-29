#pylint: disable=C0103

'''cacluations for electronics
'''
from math import (sqrt, pi)
from engnote import (eng)
from conversions import *

def lc_lowpass_cutoff():
    '''3db cutoff of an LC filter'''
    l = float(input('Inductance (H): '))
    c = float(input('Capacitance (F): '))
    a = eng((1/(2*pi*sqrt(l*c))))
    print(a, 'Hz')

def rc_lowpass_cutoff():
    '''3db cutoff of an RC filter'''
    r = float(input('Resistance (Ohms): '))
    c = float(input('Capacitance (F): '))
    a = eng((1/(2*pi*r*c)))
    print(a, 'Hz')

def capacitor_impedance():
    '''Impedance of a Capacitor'''
    freq = float(input('Frequency (Hz): '))
    c = float(input('Capacitance (F): '))
    a = eng((1/(2*pi*freq*c)))
    print(a, 'Ohms')

def inductor_impedance():
    '''Impedance of a Inductor'''
    freq = float(input('Frequency (Hz): '))
    l = float(input('Inductance (H): '))
    a = eng((2*pi*freq*l))
    print(a, 'Ohms')

def dc_voltage_divider():
    '''Voltage Divider'''
    Z1 = float(input('Impedance Top (Ohms): '))
    Z2 = float(input('Impedance Bottom (Ohms): '))
    Vin = float(input('Input Voltage (Volts): '))
    a = eng(Vin*(Z2/(Z1 + Z2)))
    print(a, 'Volts')

def ac_voltage_divider():
    '''ac voltage divider
    '''
    freq = float(input('Operating Freq (Hz): '))
    input_cap = float(input('In-Cap (F, 0 if unused): '))
    input_ind = float(input('In-Ind (H, 0 if unused): '))
    input_res = float(input('In-res (Ohms): '))

    output_cap = float(input('Out-Cap (F, 0 if unused): '))
    output_ind = float(input('Out-Ind (H, 0 if unused): '))
    output_res = float(input('Out-res (Ohms): '))
    
    Vin = float(input('Input Voltage (Vpp): '))

    Z1 = 0
    if input_cap > 0:
        Z1 = (1/(2*pi*freq*input_cap))
    elif input_ind > 0:
        Z1 = (2*pi*freq*input_ind)
    Z1 = Z1 + input_res

    Z2 = 0
    if output_cap > 0:
        Z2 = (1/(2*pi*freq*output_cap))
    elif output_ind > 0:
        Z2 = (2*pi*freq*output_ind)
    Z2 = Z2 + output_res

    a = eng(Vin*(Z2/(Z1 + Z2)))
    print(a, 'Vpp')
