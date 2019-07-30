#!/usr/bin/env python
# python 3
##  @file:                  rc2.py
#   @par:
#   @author:                Luke Gary
#   @company:
#   @date:                  2018/12/12
#   @brief:
#   @verbatim:

################################################################
# @copyright
#   Copyright 2018 [Luke Gary] as an  unpublished work.
#   All Rights Reserved.
################################################################
#/
import numpy
import scipy
import matplotlib.pyplot as plt
# %matplotlib inline
import sympy as sym
import scipy.signal as sig
import scipy.optimize as opt
from IPython.display import Image

t = sym.symbols('t')
u = sym.Function('u')(t)
x = sym.Function('x')(t)
y = sym.Function('y')(t)
R, C = sym.symbols('R C')
equations = [sym.Eq(u, R*sym.Derivative(x, t)+x/C), sym.Eq(y, x/C)]
print(equations)

s = sym.symbols('s')
U = sym.Function('U')(s)
X = sym.Function('X')(s)
Y = sym.Function('Y')(s)
L_equations = [sym.Eq(U, R*X*s+X/C), sym.Eq(Y, X/C)]
print(L_equations)

L_s = sym.solve(L_equations,Y,X)
G = L_s[Y]/U
print(G)

R_v = 10000
C_v =  100e-9
G_RC = G.subs(R, R_v).subs(C, C_v)
print(G_RC)

num = sym.Poly(sym.fraction(G_RC)[0], s).all_coeffs()
num = [float(i) for i in num]
num = numpy.array(num)
den = sym.Poly(sym.fraction(G_RC)[1], s).all_coeffs()
den = [float(i) for i in den]
den = numpy.array(den)
G_n = sig.TransferFunction(num, den)
print(G_n)

t = numpy.linspace(0, 0.1, 1000)

pwm = 3.3*(sig.square(2*numpy.pi*40*t)+1)/2
r1 = G_n.output(pwm, T=t)

cascades = []
cascades.append(r1[1])
for i in range(1,5):
    y = G_n.output(cascades[i-1], T=t)
    cascades.append(y[1])

for c in cascades:
    plt.plot(c)
plt.show()