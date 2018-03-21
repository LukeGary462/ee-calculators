#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: luke
# @Date:   2017-10-23 16:44:26
# @Last Modified by:   luke
# @Last Modified time: 2017-10-24 15:22:29

import numpy as np
import math
import argparse

print('Slew rate limited switch with P-Channel Mosfet')
print('                       Vth')
print('                       g')
print('      .--------o--------+^+--------o--------.')
print('      |        |        |||        |        |')
print('      |        |        ===        |        |')
print('      |        |    ___   |   ||   |        |')
print('      |        \'---|___|--o---||---\'        |')
print('    + |                   |   ||            |')
print('Vin  ---           Rpu   .-.     Cg         |')
print('      -                  | |              .-o-.')
print('      |                  | |              |   | RLoad')
print('      |                  \'-\' Rpd          |   |')
print('      |                   |              .-.  | CLoad')
print('      |                   |              | | ---')
print('      |                \  o              | | ---')
print('      |                 \                \'-\'  |')
print('      |                  \.               |   |')
print('      |                   o               |   |')
print('      |                   |               \'-o-\'')
print('      |                   |                 |')
print('      \'-------------------------------------\'')

def get_options():
    parser = argparse.ArgumentParser(description='calculate slew-rate limited switch')
    parser.add_argument('--gfs',nargs='?',help='Forward Transconductance',default='16')
    parser.add_argument('--vgsth',nargs='?',help='Gate Threshold Voltage',default='-1')
    parser.add_argument('--rpu',nargs='?',help='Pull Up Resistor Value',default='1e3')
    parser.add_argument('--cg',nargs='?',help='Gate Capacitor Value',default='1e-7')
    parser.add_argument('--rpd',nargs='?',help='Pull Down Resistor Value',default='470')
    parser.add_argument('--rload',nargs='?',help='Load Resistance',default='100')
    parser.add_argument('--cload',nargs='?',help='Load Capacitance',default='1e-6')
    parser.add_argument('--vin',nargs='?',help='Input Voltage',default='15')
    parser.add_argument('--t',nargs='?',help='Turn on Time',default='15e-3')

    return parser.parse_args()

if __name__ == "__main__":
    OPTIONS = get_options()

    voltage                 = float(OPTIONS.vin)
    forwardTransconductance = float(OPTIONS.gfs)
    gateThresholdVoltage    = float(OPTIONS.gfs)
    pullUpResistance        = float(OPTIONS.rpu)
    pullDownResistance      = float(OPTIONS.rpd)
    gateCapacitor           = float(OPTIONS.cg)
    loadResistance          = float(OPTIONS.rload)
    loadCapacitance         = float(OPTIONS.cload)
    turnOnTime              = float(OPTIONS.t)

    print(f'voltage                  {voltage} Volts')
    print(f'forwardTransconductance  {forwardTransconductance} Siemens')
    print(f'gateThresholdVoltage     {gateThresholdVoltage} Volts')
    print(f'pullUpResistance         {pullUpResistance} Ohms')
    print(f'pullDownResistance       {pullDownResistance} Ohms')
    print(f'gateCapacitor            {gateCapacitor} Farads')
    print(f'loadResistance           {loadResistance} Ohms')
    print(f'loadCapacitance          {loadCapacitance} Farads')
    print(f'turnOnTime               {turnOnTime} Seconds')