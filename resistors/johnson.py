#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: luke
# @Date:   2017-10-16 14:05:11
# @Last Modified by:   luke
# @Last Modified time: 2018-11-16 15:31:08
import numpy as np
import math
import argparse

BOLTZMAN = 1.38065e-23

def get_options():
    parser = argparse.ArgumentParser(description='calculate johnson-nyquist noise in resistors and caps')
    parser.add_argument('--type','-t',nargs='?',help='[iin|res]',default='res')
    parser.add_argument('--temperature',nargs='?',help='temp in C', default='27.0')
    parser.add_argument('--iin',nargs='?',help='input noise current', default='1e-12')
    parser.add_argument('--value','-v',nargs='+',help='value of component',default='1.0')
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
        rmss = []
        for r in OPTIONS.value:
            uVrms = resistor_vrms(tempC_to_tempK(float(OPTIONS.temperature)), float(r), float(OPTIONS.bandwidth)) * 1e6
            uVpp = vrms_to_vpp(uVrms)
            print(f'Res:{r} Ohms, BW:{OPTIONS.bandwidth} Hz, eVrms:{uVrms:.6f} uV, eVpp:{uVpp:.6f} uV')
            rmss.append(uVrms)
        total = 0
        for v in rmss:
            total += math.pow(v,2)
        total = math.sqrt(total)
        print(f'Total RMS noise is {total:.6f}uVrms')
        print(f'Total VPP noise is {vrms_to_vpp(total):.6f}uVpp')
    elif OPTIONS.type == 'iin':
        uVrms = float(OPTIONS.value)*float(OPTIONS.iin) * math.sqrt(float(OPTIONS.bandwidth)) * 1e6
        uVpp = vrms_to_vpp(uVrms)
        print(f'[{OPTIONS.iin}A/rt-Hz]\teVrms:{uVrms}, eVpp:{uVpp}')
    else:
        print('option not implemented')


