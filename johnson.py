#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: luke
# @Date:   2017-10-16 14:05:11
# @Last Modified by:   luke
# @Last Modified time: 2017-10-16 16:24:14
import numpy as np
import math
import argparse

BOLTZMAN = 1.38e-23

def get_options():
    parser = argparse.ArgumentParser(description='calculate johnson-nyquist noise in resistors and caps')
    parser.add_argument('--type','-t',nargs='?',help='[iin|res]',default='res')
    parser.add_argument('--temperature',nargs='?',help='temp in C', default='27.0')
    parser.add_argument('--iin',nargs='?',help='input noise current', default='1e-12')
    parser.add_argument('--value','-v',nargs='?',help='value of component',default='1.0')
    parser.add_argument('--bandwidth', '-b',nargs='?',help='signal bandwidth',default='1000000')
    return parser.parse_args()

def tempC_to_tempK(tempCelsius):
    return 273.15 + tempCelsius

def resistor_vrms(temperatureKelvin, resistance, bandwidth):
    return math.sqrt((4 * BOLTZMAN)*temperatureKelvin*resistance*bandwidth)

def vrms_to_vpp(vrms):
    return 6.6 * vrms;

if __name__ == "__main__":
    OPTIONS = get_options()

    if OPTIONS.type == 'res':
        vrms = resistor_vrms(tempC_to_tempK(float(OPTIONS.temperature)), float(OPTIONS.value), float(OPTIONS.bandwidth))
        vpp = vrms_to_vpp(vrms)
        print(f'[{OPTIONS.value} Ohms]\teVrms:{vrms}, eVpp:{vpp}')
    elif OPTIONS.type == 'iin':
        vrms = float(OPTIONS.value)*float(OPTIONS.iin) * math.sqrt(float(OPTIONS.bandwidth))
        vpp = vrms_to_vpp(vrms)
        print(f'[{OPTIONS.iin}A/rt-Hz]\teVrms:{vrms}, eVpp:{vpp}')
    else:
        print('option not implemented')