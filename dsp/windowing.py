#!/usr/bin/env python
# python 3
#pylint: disable=
##    @file:    windowing.py
#     @name:    Luke Gary
#  @company:    <company>
#     @date:    2021/6/4
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
windowing functions
"""
import math

class Window:
    '''rectangular window base'''
    def __init__(self, **kwargs):
        '''init'''
        self.N = kwargs.get('N', 1)
        self._counter = 0

    def calculate(self, x, y):
        '''update func , this will be overloaded'''
        return y

    def update(self, value):
        '''run the window network'''
        output = self.calculate(self._counter, value) 
        self._counter += 1
        if self._counter >= self.N:
            self._counter = 0
        return output

    def reset(self):
        self._counter = 0

class TriangularWindow(Window):
    '''triangular window where L=N'''
    def __init__(self, **kwargs):
        super().__init__(
            N=kwargs.get('N', 0)
        )

    def calculate(self, x, y):
        '''calculate triangular window'''
        wn = 1.0 - abs((x - (self.N-1.0)/2.0) / (self.N/2.0))
        return y*wn

class FlatTopWindow(Window):
    ''' 
        flat top window function
        High amplitude accuracy at the expense of ENBW and
        frequency resolution
        The normalized equivalent noise bandwidth of this window is 3.8193596 Hz-sec
        Use for fixed sinusoidal sources
    '''
    def __init__(self, **kwargs):
        super().__init__(
            N=kwargs.get('N', 0)
        )

    def calculate(self, x, y):
        '''calculate flat top window'''
        wn0 = 1.930 * math.cos((2.0*math.pi*self._counter)/(self.N))
        wn1 = 1.290 * math.cos((4.0*math.pi*self._counter)/(self.N))
        wn2 = 0.388 * math.cos((6.0*math.pi*self._counter)/(self.N))
        wn3 = 0.028 * math.cos((8.0*math.pi*self._counter)/(self.N))
        return y * (1.0 - wn0 + wn1 - wn2 + wn3)

class BlackmanHarrisWindow(Window):
    '''blackman-harris'''
    def __init__(self, **kwargs):
        super().__init__(
            N=kwargs.get('N', 0)
        )

    def calculate(self, x, y):
        '''calculate'''
        wn0 = 0.48829 * math.cos((2.0*math.pi*self._counter)/(self.N))
        wn1 = 0.14128 * math.cos((4.0*math.pi*self._counter)/(self.N))
        wn2 = 0.01168 * math.cos((6.0*math.pi*self._counter)/(self.N)) 
        return y * (1.0 - wn0 + wn1 - wn2)

class NuttallWindow(Window):
    '''nuttall window'''
    def __init__(self, **kwargs):
        super().__init__(
            N=kwargs.get('N', 0)
        )

    def calculate(self, x, y):
        '''calculate'''
        wn0 = 0.4891775 * math.cos((2.0*math.pi*self._counter)/(self.N))
        wn1 = 0.1365995 * math.cos((4.0*math.pi*self._counter)/(self.N))
        wn2 = 0.0106411 * math.cos((6.0*math.pi*self._counter)/(self.N)) 
        return y * (0.3635819 - wn0 + wn1 - wn2)

class BlackmanNuttall(Window):
    '''blackman nuttall'''
    def __init__(self, **kwargs):
        super().__init__(
            N=kwargs.get('N', 0)
        )

    def calculate(self, x, y):
        '''calculate'''
        wn0 = 0.4891775 * math.cos((2.0*math.pi*self._counter)/(self.N))
        wn1 = 0.1365995 * math.cos((4.0*math.pi*self._counter)/(self.N))
        wn2 = 0.0106411 * math.cos((6.0*math.pi*self._counter)/(self.N)) 
        return y * (1.0 - wn0 + wn1 - wn2)

class HammingWindow(Window):
    '''hamming window (25/46) - 0.46 * cos(2*pi*n/N)'''
    def __init__(self, **kwargs):
        super().__init__(
            N=kwargs.get('N', 0)
        )

    def calculate(self, x, y):
        '''calculate'''
        return y * ((25/46) - (0.46*math.cos(2*math.pi*(x/self.N))))

class HanningWindow(Window):
    '''hanning window'''
    def __init__(self, **kwargs):
        super().__init__(
            N=kwargs.get('N', 0)
        )

    def calculate(self, x, y):
        '''calculate'''
        return y * (0.5 - (0.5*math.cos(2*math.pi*(x/self.N))))



WINDOW_FUNCS = {
    'triangular': TriangularWindow,
    'flat-top': FlatTopWindow,
    'blackman-harris': BlackmanHarrisWindow,
    'blackman-nuttall': BlackmanNuttall,
    'hamming': HammingWindow,
    'hanning': HanningWindow,
    'nuttall': NuttallWindow,
    'rectangular': Window,
}

def evaluate_windows(windows=None, length=1000):
    '''return a dict of window function responses
    based on key list'''

    output = {
    }
    for wkey in windows:
        wn = WINDOW_FUNCS.get(wkey, Window)(N=length)
        y = []
        x = []
        for i in range(length):
            x.append(i) 
            y.append(wn.calculate(i, 1.0))
        wn.reset()
        output[wkey] = (
            x,
            y
        )
    return output

def apply_window_to_block(data, window_type=None):
    ''' apply a window to the data argument '''
    wt = WINDOW_FUNCS.get(window_type, None)
    output = []
    if isinstance(data, list) and wf:
        wf = wt(N=len(data))
        output = [
            wf.calculate(x)
            for x in data
        ]
    return output

