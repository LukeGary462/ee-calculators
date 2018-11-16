#!/usr/bin/env python
# python 3
##  @file:                  lpf.py
#   @par:
#   @author:                Luke Gary
#   @company:               RyeEffectsResearch
#   @date:                  2018/4/30
#   @brief:
#   @verbatim:
#   @note:                  http://www.ti.com/lit/an/sloa024b/sloa024b.pdf
#                           http://www.analog.com/en/analog-dialogue/articles/phase-relations-in-active-filters.html

################################################################
# @copyright
#   Copyright 2018 [RyeEffectsResearch] as an  unpublished work.
#   All Rights Reserved.
#
# @license The information contained herein is confidential
#   property of [RyeEffectsResearch]. The user, copying, transfer or
#   disclosure of such information is prohibited except
#   by express written agreement with [RyeEffectsResearch].
################################################################
#/

import numpy as np
import scipy as scy
import math
import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def get_options():
    parser = argparse.ArgumentParser(description='calculate filter values')
    parser.add_argument('--type','-t',nargs='+',help='[rc|sallen-key]',default=['rc'])
    parser.add_argument('--job','-j',nargs='+',help='[solve|plot]',type=str,default=['plot', 'cap'])
    parser.add_argument('--resistance', '-r', nargs='?', type=float, default=10e3)
    parser.add_argument('--capacitance', '-c', nargs='?', type=float, default=1e-9)
    parser.add_argument('--frequency-max', '-fmax', nargs='?', type=float, default=100e6)
    parser.add_argument('--frequency-cut', '-fcut', nargs='?', type=float, default=1e6)
    parser.add_argument('--plot','-p',action='store_true',default=False)
    parser.add_argument('--loglog', '-ll',action='store_true',default=False)
    return parser.parse_args()

def map_filter_type_to_solver(type):
    switch = {
        'rc': solve_rc,
        'sallen-key': solve_sallen_key,
    }
    return switch.get(type, -1)

def mapp_type_to_img(type):
    switch = {
        'rc': 'img/lp-1-rc.png',
        'sallen-key': 'img/lp-sk.png',
    }
    return switch.get(type, -1)

def map_filter_type_to_plotter(type):
    switch = {
        'rc': plot_rc,
        'sallen-key': plot_sallen_key,
    }
    return switch.get(type, -1)

def solve_rc(solve, Fc, R, C):
    if solve[0] == 'c':
        C = (1.0/Fc) / (2*np.pi*R)
    else:
        R = (1.0/Fc) / (2*np.pi*C)
    return R, C

def plot_rc(Fc, Fm, R, C):
    F       = np.geomspace(0.1, Fm, dtype=float)
    Xc      = np.empty_like(F)
    gain    = np.empty_like(F)
    phase   = np.empty_like(F)
    a       = np.empty_like(F)
    fc      = 1.0 / (2*np.pi*R*C)
    #solve gain
    for i in range(0, len(F)):
        #cap reactance
        Xc[i] = 1 / (2*np.pi*F[i]*C)
        #gain
        a[i] = Xc[i] / ( np.sqrt( np.power(R,2) + np.power(Xc[i],2) ) )
        gain[i] = 20*np.log10(a[i])
        phase[i] = (-1.0*np.arctan(2*np.pi*F[i]*R*C))*(90.0/np.pi)

    return a, phase, F, fc

def solve_sallen_key(solve, Fc, R, C):
    # assume R1 = R2, and C1 = C2
    if solve[0] == 'c':
        C = np.power(((1.0/Fc) / (2*np.pi)),2)/R
    else:
        R = np.power(((1.0/Fc) / (2*np.pi)),2)/C
    return R, C

def plot_sallen_key(Fc, Fm, R, C):
    F       = np.geomspace(0.1, Fm, dtype=float)
    Xc      = np.empty_like(F)
    gain    = np.empty_like(F)
    phase   = np.empty_like(F)
    a       = np.empty_like(F)
    fc      = 1.0 / ((2*np.pi)*( np.sqrt(R*R*C*C) ) )
    Q       = np.sqrt(R*R*C*C) / (C*2*R)
    alpha   = ((fc*2*np.pi)/Q)/2
    #solve gain
    for i in range(0, len(F)):
        #cap reactance
        Xc[i] = 1 / (2*np.pi*F[i]*C)
        #gain
        numerator = Xc[i] * Xc[i]
        denomenator = (R+R) + (Xc[i]*(R+R)) + (Xc[i]*Xc[i])
        a[i] = numerator / denomenator
        p = -1.0*np.arctan((1/alpha)*((2*2*np.pi*F[i]/fc)+(np.sqrt(4-np.power(alpha,2)))))
        phase[i] = p - p

    return a, phase, F, fc



if __name__ == "__main__":
    OPTIONS = get_options()

    plt.figure()
    for archType in OPTIONS.type:
        cutoff = OPTIONS.frequency_cut
        maxFrequency = OPTIONS.frequency_max
        res = OPTIONS.resistance
        cap = OPTIONS.capacitance

        if OPTIONS.job[0] == 'solve':
            solver = map_filter_type_to_solver(archType)
            res, cap = solver(OPTIONS.job[1], cutoff, res, cap)

        print(f'SOLVE R: {res} Ohms')
        print(f'SOLVE C: {cap} Farads')
        plotter = map_filter_type_to_plotter(archType)
        gain, phase, frequencies, fc = plotter(cutoff, maxFrequency, res, cap)

        print(f'f-3dB:{fc} Hz')
        print(f'GAIN:{gain} 1.0/1.0')
        print(f'PHASE:{phase}')


        if OPTIONS.plot == True:
            plt.subplot(221)
            img = mpimg.imread(mapp_type_to_img(archType))
            plt.imshow(img)

            plt.suptitle(f'{archType} Filter, [{cutoff}Hz : 0Hz-{maxFrequency}Hz], [{res}Ohms:{cap}Farads]')
            plt.subplot(222)
            plt.title('Gain')
            if OPTIONS.loglog == True:
                plt.loglog(frequencies, gain, label=archType)
            else:
                plt.semilogx(frequencies, gain, label=archType)
            plt.axvline(fc, color='r')
            plt.grid(True, which='major')
            plt.grid(True, which='minor')
            plt.minorticks_on()

            plt.subplot(224)
            plt.title('Phase')
            plt.semilogx(frequencies, phase, label=archType)
            plt.axvline(fc, color='r')
            plt.grid(True, which='major')
            plt.grid(True, which='minor')
            plt.minorticks_on()

    if OPTIONS.plot == True:
        plt.legend(loc='best')
        plt.show()
