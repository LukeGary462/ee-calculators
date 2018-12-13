#!/usr/bin/env python
# python 3
##  @file:                  t.py
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
import scipy.signal as signal
import scipy.optimize as opt

duration=1.0 #1sec
dT=1e-6
freq=1e3
eDuty=0.25

t = np.arange(0, duration, dT, dtype=float)
plt.plot(t, signal.square(2 * np.pi * freq * t, duty=eDuty))
plt.ylim(-2, 2)
plt.figure()
sig = np.sin(2 * np.pi * t)
pwm = signal.square(2 * np.pi * 30 * t, duty=(sig + 1)/2)
plt.subplot(2, 1, 1)
plt.plot(t, sig)
plt.subplot(2, 1, 2)
plt.plot(t, pwm)
plt.ylim(-1.5, 1.5)
plt.show()