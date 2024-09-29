#!/usr/bin/env python
# python 3
##    @file:    utils.py
#     @name:    Luke Gary
#  @company:    <company>
#     @date:    2021/2/19
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
{ high-level module description }
"""
import math

APPROX_ZERO = 1e-20

def linspace(start, stop, step=100):
    '''evenly spaced values from start to stop'''
    if step < 2:
        return start
    diff = (float(stop) - start)/(step - 1)
    return [diff * i + start for i in range(step)]

def min_clip(value, minval):
    if isinstance(value, (int, float)):
        value = [value]

    result = [
        minval if x <= 0  else x 
        for x in value
    ]

    if len(result) == 1:
        return result[0]
    return result


def safe_log10(operand, minval=APPROX_ZERO):
    '''safe base 10 log'''
    return math.log10(min_clip(operand, minval))


if __name__ == '__main__':
    import numpy as np
    print(min_clip(0.0, 0.01))
    print(min_clip(0, 0.01))
    print(min_clip(-0.0, 0.01))
    print(min_clip(-0, 0.01))
    print(min_clip([-1, 0, 1, 2], 0.01))
    print(min_clip([-1.0, 0.0, 1.0, 2.0], 0.01))
    print(min_clip(np.asarray([-1, 0, 1, 2]), 0.01))
    print(min_clip(np.asarray([-1.0, 0.0, 1.0, 2.0]), 0.01))

