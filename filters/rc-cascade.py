#!/usr/bin/env python
# python 3
##  @file:                  rc-cascade.py
#   @par:
#   @author:                Luke Gary
#   @company:               Biomeme, Inc
#   @date:                  2018/12/12
#   @brief:
#   @verbatim:

################################################################
# @copyright
#   Copyright 2018 [Biomeme, Inc] as an  unpublished work.
#   All Rights Reserved.
#
# @license The information contained herein is confidential
#   property of [Biomeme, Inc]. The user, copying, transfer or
#   disclosure of such information is prohibited except
#   by express written agreement with [Biomeme, Inc].
################################################################
#/

import numpy as np
import scipy as scy
import math
import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import sympy as sym
import scipy.signal as sig
import scipy.optimize as opt
from ewma import *

def get_options():
    parser = argparse.ArgumentParser(description='calculate filter values')
    parser.add_argument('-v', '--values', type=str, default='[(700,1e-7)]', help='list of tuples. [(R, C), ...]')
    parser.add_argument('-r', '--repeats', type=int, default=1)
    parser.add_argument('-p', '--plot', action='store_true', help='plot data')
    parser.add_argument('-dt', '--timestep', type=float, default=1e-6, help='timestep to calculate simulation')
    parser.add_argument('-d', '--duration', type=float, default=1.0, help='length of time to run simulation')
    parser.add_argument('-ef', '--freq', type=float, default=1e3, help='freqency of signal to put through network')
    parser.add_argument('-eD', '--delay', type=float, default=0.0)
    parser.add_argument('-ed', '--duty', type=float, default=0.5, help='duty cycle of square excitation signal')
    parser.add_argument('-el', '--low', type=float, default=0.0)
    parser.add_argument('-eh', '--high', type=float, default=1.0)
    return parser.parse_args()

if __name__ == "__main__":
    opt = get_options()

    #get values
    values = eval(opt.values)

    #calculate transfer functions for each stage
    tfs = []
    cnt = 1
    for i in range(0, opt.repeats):
        for v in values:
            stage = {}
            print(f'RC Stage {cnt}')
            t = sym.symbols('t')
            u = sym.Function('u')(t)
            x = sym.Function('x')(t)
            y = sym.Function('y')(t)
            R, C = sym.symbols('R C')
            equations = [sym.Eq(u, R*sym.Derivative(x, t)+x/C), sym.Eq(y, x/C)]
            # print(f'u(t): {equations}')

            s = sym.symbols('s')
            U = sym.Function('U')(s)
            X = sym.Function('X')(s)
            Y = sym.Function('Y')(s)
            L_equations = [sym.Eq(U, R*X*s+X/C), sym.Eq(Y, X/C)]
            # print(f'Laplace(u(t)): {L_equations}')

            L_s = sym.solve(L_equations,Y,X)
            G = L_s[Y]/U
            # print(f'g(t): {G}')

            R_v =   float(v[0])
            C_v =   float(v[1])
            G_RC = G.subs(R, R_v).subs(C, C_v)
            # print(f'g(t)-rc: {G_RC}')

            num = sym.Poly(sym.fraction(G_RC)[0], s).all_coeffs()
            num = [float(i) for i in num]
            num = np.array(num)
            den = sym.Poly(sym.fraction(G_RC)[1], s).all_coeffs()
            den = [float(i) for i in den]
            den = np.array(den)
            G_n = sig.TransferFunction(num, den)
            # print(f'H(s): {G_n}')

            stage['eq']     = equations
            stage['L-eq']   = L_equations
            stage['G']      = G
            stage['Grc']    = G_RC
            stage['Gn']     = G_n
            stage['order']  = cnt
            stage['coef']   = opt.timestep/(R_v * C_v + opt.timestep)
            tfs.append(stage)
            cnt += 1

    #create time scale and excitation signal for time-domain plot
    t   = np.arange(0, opt.duration, opt.timestep, dtype=float)
    V = sig.square(2*np.pi * opt.freq * t + opt.delay, duty=opt.duty)
    V = ((V * 0.5) +0.5)
    v0 = []
    for v in V:
        if v >= 1.0:
            v0.append(opt.high)
        else:
            v0.append(opt.low)

    v0 = np.asarray(v0)

    voltages = []
    x = {}
    x['y'] = v0
    x['order'] = 0
    voltages.append(x)
    #calculate outputs
    for i in range(1,len(tfs)+1):
        print(f"{tfs[i-1]['order']} - {tfs[i-1]['Grc']} - alpha equivalent {tfs[i-1]['coef']}")
        output = tfs[i-1]['Gn'].output(voltages[i-1]['y'], T=t)
        o = {}
        o['y'] = output[1]
        o['order'] = tfs[i-1]['order']
        voltages.append(o)

    plt.figure()
    plt.plot(t, voltages[0]['y'])

    plt.figure()
    for v in voltages:
        plt.plot(t, v['y'], label=f"Stage-{v['order']}")

    # #model the cascade rc simulation with an ewma cascade based on calculated alphas
    # coeff = []
    # for t in tfs:
    #     coeff.append(t['coef'])
    # filt = EWMA(coeff, 0.0)
    # modelOutput = []
    # for v in v0:
    #     modelOutput.append(filt.calculate(v))
    # modelOutput = np.asarray(modelOutput)

    # plt.plot(t, modelOutput, label='EWMA-Model')

    plt.text(0.35,0.5,opt.values, fontsize=14, verticalalignment='center', horizontalalignment='left', family='monospace')
    plt.ylim(opt.low, opt.high)
    plt.grid()
    plt.legend(loc='best')
    plt.show()
