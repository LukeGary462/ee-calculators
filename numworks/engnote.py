"""
Created on Wed Aug 08 15:49:13 2012

@author: Cambium
"""
from math import (floor, log10)

def powerise10(value):
    """ Returns value as a * 10 ^ b with 0<= a <10
    """
    if value == 0: return 0 , 0
    _neg = value <0
    if _neg : value = -value
    _a = 1.0 * value / 10**(floor(log10(value)))
    _b = int(floor(log10(value)))
    if _neg : _a = -_a
    return _a ,_b
    
def eng(value):
    """Return a string representing value in an engineer friendly notation"""
    _a , _b = powerise10(value)
    if -3<_b<3: return "%.4g" % value
    _a = _a * 10**(_b%3)
    _b = _b - _b%3
    return "%.4g*10^%s" %(_a,_b)
    