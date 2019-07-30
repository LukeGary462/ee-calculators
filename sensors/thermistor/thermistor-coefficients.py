#!/usr/bin/env python
# python 3
##  @file:                  thermistor-coefficients.py
#   @par:
#   @author:                Luke Gary
#   @company:               Biomeme, Inc
#   @date:                  2019/6/28
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
#/

import numpy as np
import matplotlib.pyplot as plt
import argparse

def get_options():
    parser = argparse.ArgumentParser(description='Calculate Thermistor coeff (A,B,C) from 3 temperature points')
    parser.add_argument('-t', '--temps', type=float, nargs=3, help='List of temp samples')
    parser.add_argument('-r', '--resistances', type=float, nargs=3, help='list of resistance samples')
    parser.add_argument('-v', '--voltage', type=float, default=3.3, help='Ref Voltage for Divider simulation')
    parser.add_argument('-rd', '--divider-resistance', type=float, help='resistance of divider resistor to ground')
    parser.add_argument('-cv','--calc-voltage', action='store_true')
    parser.add_argument('-cf', '--calc-fits', action='store_true')
    parser.add_argument('-fo', '--fit-order', type=int, default=3)
    return parser.parse_args()


def calculate_steinhart_coeff(args):
    temps = args.temps
    res = args.resistances

    L1 = np.log(res[0])
    Y1 = 1/temps[0]
    L2 = np.log(res[1])
    Y2 = 1/temps[1]
    L3 = np.log(res[2])
    Y3 = 1/temps[2]

    gamma2 = (Y2-Y1)/(L2-L1)
    gamma3 = (Y3-Y1)/(L3-L1)

    C = ((gamma3-gamma2)/(L3-L2)) * (1/(L1+L2+L3))
    B = gamma2 - C*(L1**2 + L1*L2 + L2**2)
    A = Y1 - (B + L1**2 * C)*L1

    return [A,B,C]

def calculate_steinhart_res(coeff, temp):
    a = coeff[0]
    b = coeff[1]
    c = coeff[2]

    x = (1/(2*c)) * (a - (1/temp))
    z = (b/(3*c))**3 + x**2
    y = np.sqrt(z)

    root1 = np.cbrt(y-x)
    root2 = np.cbrt(y+x)
    r = np.exp(root1-root2)
    return r

def calculate_v_from_div(r1, r2, vref):
    return (vref*(r1/r1*r2))

def calculate_beta_res(beta, ro, to, temp):
    rinf = ro * np.exp(-1.0*beta/to)
    res = rinf * np.exp(beta/temp)
    return res

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def find_nearest_index(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx


if __name__ == '__main__':
    args = get_options()

    coeff = calculate_steinhart_coeff(args)
    print(coeff)

    t = args.temps
    r = args.resistances
    for i in range(len(r)):
        print(r[i], calculate_steinhart_res(coeff, r[i]))

    ts = np.arange(25, 100, 0.01)
    rs = calculate_steinhart_res(coeff, ts)

    plt.figure()
    plt.plot(ts,rs)


    #test with NCP15XH103F03RC simulation
    beta_25_100 = 3455
    rs = calculate_beta_res(beta_25_100, 10e3, 25.0, ts)
    i1 = find_nearest_index(ts, 30.0)
    i2 = find_nearest_index(ts, 60.0)
    i3 = find_nearest_index(ts, 95.0)

    t = [ts[i1], ts[i2], ts[i3]]
    r = [rs[i1], rs[i2], rs[i3]]
    args.temps = t
    args.resistances = r
    coeff = calculate_steinhart_coeff(args)
    print(coeff)
    rs1 = calculate_steinhart_res(coeff, ts)
    plt.figure()
    plt.plot(ts,rs)
    plt.plot(ts,rs1)

    plt.show()