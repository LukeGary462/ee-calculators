#!/usr/bin/env python
# python 3
# @file:                  ntc-model.py
#   @par:
#   @author:                Luke Gary
#   @company:               Biomeme, Inc
#   @date:                  2019/7/2
#   @brief:
#   @verbatim:

################################################################
# @copyright
#   Copyright 2019 [Biomeme, Inc] as an  unpublished work.
#   All Rights Reserved.
#
# @license The information contained herein is confidential
#   property of [Biomeme, Inc]. The user, copying, transfer or
#   disclosure of such information is prohibited except
#   by express written agreement with [Biomeme, Inc].
################################################################
# /

import argparse
import scipy.optimize as opt
import numpy as np
import matplotlib.pyplot as plt

# All NTC's at 25C must be 10K Ohm


def get_args():
    parser = argparse.ArgumentParser(
        description='Calculate various Thermistor models with csv input dataset (Voltage Vs Temp) T0 @25C = 10KOhm')
    parser.add_argument('files', nargs='+', help='input file list')
    parser.add_argument('-p', '--plot', action='store_true')
    parser.add_argument('--mt', '--model-type', default='poly', help='model type, [poly | rational]')
    parser.add_argument('-po', '--poly-order', type=int, default=4, help='order of polynomials used')

    return parser.parse_args()

def noise(amplitude, size):
    return amplitude*(np.random.uniform(-1.0,1.0, size=size))

def get_data(file):
    f = open(file, 'r')
    output = {}
    output['t'] = []
    output['v'] = []
    for line in f:
        # print(line)
        if '#' in line:
            continue
        if ',' in line:
            line = line.split(',')
            output['v'].append(float(line[0]))
            output['t'].append(float(line[1]))

    output['v'] = np.asarray(output['v'])
    output['t'] = np.asarray(output['t'])
    return output

def rat_5(x, c1, c2, c3, c4, c5):
    To = 25.0
    num = x*(c1 + x*(c2 + x*c3))
    dem = 1.0 + x*(c4 + x*c5)
    return To + (num/dem)

def poly_5(x, c1, c2, c3, c4, c5):
    return (1 + x*(c2 + x*(c3 + x*(c4 + x*c5)))) + 25.0

def rat_4(x, c1, c2, c3, c4, c5):
    To = 25.0
    num = x*(c1 + x*(c2 + x*c3))
    dem = 1.0 + x*(c4 + x*c5)
    return To + (num/dem)

def poly_4(x, c1, c2, c3, c4):
    return (c1 + x*(c2 + x*(c3 + x*c4))) + 25.0

if __name__ == '__main__':
    args = get_args()

    for file in args.files:
        data = get_data(file)
        volts = data['v']  + noise(0.01, size=len(data['v']))
        temps = data['t']

        rp0 =  [1.0,1.0,1.0,1.0,1.0]
        pp0 =  [1.0,1.0,1.0,1.0,1.0]

        bounds = ([-200,-200,-200,-200,-200],[200,200,200,200,200])

        try:
            ratco, ratcov = opt.curve_fit(rat_5, volts, temps, p0=rp0, bounds=bounds)
        except:
            print('rat5 fail')
            ratco = rp0

        polyco = np.polyfit(volts, temps, 5)

        print('5th-poly: ', polyco)
        print(' 5th-rat: ', ratco)

        plt.figure()
        plt.plot(temps, volts, '-', label='Ideal')
        plt.ylim((0.0, 3.3))
        plt.plot(temps, rat_4(temps, *ratco), label='RAT5', linestyle='--')
        # plt.plot(temps, , label='POLY5', linestyle='--')
        plt.legend('loc=best')
        plt.show()


