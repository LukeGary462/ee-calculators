#!/usr/bin/env python
# python 3
##  @file:                  rmss.py
#   @par:
#   @author:                Luke Gary
#   @company:               Biomeme, Inc
#   @date:                  2018/11/16
#   @brief:
#   @verbatim:

################################################################
# @copyright
#   Copyright 2018 Rye Effects Research as an  unpublished work.
#   All Rights Reserved.
#
# @license The information contained herein is confidential
#   property of Rye Effects Research. The user, copying, transfer or
#   disclosure of such information is prohibited except
#   by express written agreement with Rye Effects Research.
################################################################
#/

import argparse
import numpy as np
import math

def get_options():
    parser = argparse.ArgumentParser(description='calculate johnson-nyquist noise in resistors and caps')
    parser.add_argument('-v','--values', nargs='+')
    return parser.parse_args()

opt = get_options()

L=0.0

for v in opt.values:
    L += math.pow(float(v),2)
T=math.sqrt(L)
print(f'{T}')
print('')
i=1
for v in opt.values:
    print(f'RMS Value {i:2} {float(v):.8f} Volts rms')
    i+=1
print(f'     RMS Sum is ~ {T} Vrms')
print(f'Peak-to-Peak is ~ {T*6.6} Vpp')

