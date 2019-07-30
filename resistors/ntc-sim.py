#!/usr/bin/env python
# python 3
##  @file:                  ntc-sim.py
#   @par:
#   @author:                Luke Gary
#   @company:               Biomeme, Inc
#   @date:                  2018/8/24
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
import matplotlib.pyplot as plt
import numpy as np

def rNtc(beta, To, Ro, T):
    return Ro * (np.exp(beta * ((1.0/(T+(273.15))-(1.0/(To+(273.15)))))))


plt.figure()

R0  = 10e3 # R at T0
T0  = 25   # temperature at R0
B   = 3455 # kelvin beta

temp = np.arange(T0, 100, 0.5, dtype=float)
r = np.zeros_like(temp)

for t in range(0, len(temp)):
    r[t] = rNtc(B,T0,R0, temp[t])

plt.plot(temp, r)

plt.figure()

Vin = 5.0
Rb = 10e3

v = np.zeros_like(temp)
for t in range(0, len(temp)):
    v[t] = Vin*(Rb/(Rb+r[t]))

plt.plot(temp, v)

plt.show()
