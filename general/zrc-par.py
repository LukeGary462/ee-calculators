#!/usr/bin/env python
# python 3
#pylint: disable=
##    @file:    zrc-par.py
#     @name:    Luke Gary
#  @company:    <company>
#     @date:    2021/10/14
################################################################################
# @copyright
#   Copyright 2020 <company> as an  unpublished work.
#   All Rights Reserved.
#
# @license The information contained herein is confidential
#   property of <company>. The user, copying, transfer or
#   disclosure of such information is prohibited except
#   by express written agreement with <company>.
################################################################################

"""
Parallel RC Impedance
TODO: Ylimit for plots, grids, convert to subplots with linked axis
"""
import numpy as np
import matplotlib.pyplot as plt
from argparse import ArgumentParser

def get_options():
    parser = ArgumentParser(description='calculate Parallel RC Impedance')
    parser.add_argument('--temperature',nargs='?',help='temp in C', default=27.0)
    parser.add_argument('--freq', '-f',help='signal freq',default=1e3)
    parser.add_argument('-r', default=1e3)
    parser.add_argument('-c', default=1e-6)
    parser.add_argument('-p', '--plot', action='store_true')
    parser.add_argument('-bw', nargs='+', default=[0.01, 100.0e3])
    return parser.parse_args()

def run(args, freq, echo=False):
    '''calculate the impedance of the RC network'''
    res = args.r 
    cap = args.c 
    w = 2*np.pi*freq
    xc = (1/(w*cap))
    zrc = 1/np.sqrt(
        (1/res)**2 + (w*cap)**2
    )
    phase_shift = np.arctan(-1.0*w*cap*res) * (180/np.pi)

    if echo:
        cap_u = cap / 1.0e-6
        print(f'{res} Ohm || {cap_u} uF @{freq}Hz : Xc = {xc:0.5f} Ohm, Zrc = {zrc:0.5f}, phase = {phase_shift:0.5f} deg')
    
    return xc, zrc, phase_shift

if __name__ == '__main__':
    args = get_options()
    if args.plot:
        xcs = []
        zrcs = []
        ws = []
        freqs = np.linspace(args.bw[0], args.bw[1], 100000)
        for f in freqs:
            res = run(args, freq=f)
            xcs.append(res[0])
            zrcs.append(res[1])
            ws.append(res[2])

        res = args.r 
        cap = args.c 
        cap_u = cap / 1.0e-6
        plt.figure('Xc vs Freq')
        plt.title(f'Xc for {res} Ohm || {cap_u} uF from {args.bw[0]}Hz to {args.bw[0]}Hz')
        plt.semilogx(freqs, xcs)

        plt.figure('Zrc vs Freq')
        plt.title(f'Zrc for {res} Ohm || {cap_u} uF from {args.bw[0]}Hz to {args.bw[0]}Hz')
        plt.semilogx(freqs, zrcs)

        plt.figure('Phase vs Freq')
        plt.title(f'Phase for {res} Ohm || {cap_u} uF from {args.bw[0]}Hz to {args.bw[0]}Hz')
        plt.semilogx(freqs, ws)

        plt.show()

    else:
        run(args, freq=args.freq, echo=True)