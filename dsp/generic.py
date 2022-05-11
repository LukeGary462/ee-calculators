#!/usr/bin/env python
# python 3
##    @file:    generic.py
#     @name:    Luke Gary
#  @company:    Rye Effects Research
#     @date:    2021/2/17
################################################################################
# @copyright
#   Copyright 2020 Rye Effects Research as an  unpublished work.
#   All Rights Reserved.
#
# @license The information contained herein is confidential
#   property of Rye Effects Research. The user, copying, transfer or
#   disclosure of such information is prohibited except
#   by express written agreement with Rye Effects Research.
################################################################################

"""
generic DSP network
http://homepages.cae.wisc.edu/~ece734/references/lyons.pdf
All credit to Richard Lyons and Amy Bell, Im just writing
a python module that shows their work!
"""
import math
from typing import Tuple
from utils import linspace, safe_log10, APPROX_ZERO

class SimpleIIR:
    '''iir filter, 1 add, 2 multiply, 1 delay register'''
    def __init__(self, **kwargs):
        '''init'''
        N = kwargs.get('N', 10)
        self.b0 = 1.0 / N
        self.a1 = N - 1.0
        self.last_output = kwargs.get('ic', 0.0)

    def update(self, sample):
        '''update filter with new sample'''
        output = (sample + self.last_output*self.a1)*self.b0
        self.last_output = output 
        return output

    def reset(self, ic=0.0):
        '''reset filter'''
        self.last_output = ic

class FirstOrderIIR:
    def __init__(self, fc, fs):
        theta_c = 2.0*math.pi*(fc/fs)
        self.fc = fc
        self.fs = fs
        self.gamma = math.cos(theta_c) / (1.0 + math.sin(theta_c))
        self.alpha_hp = (1.0 + self.gamma) / 2.0
        self.alpha_lp = (1.0 - self.gamma) / 2.0
        self.last_input = 0
        self.last_output = 0

    # def evaluate_at_frequency(self, freq: float, sample_rate: float) -> Tuple:
    #     '''placeholder'''
    #     return (1, 0)

    def get_frequency_response(self, freq_range, **options) -> Tuple:
        """
        Gets the frequency response for a given range of frequencies

        :param      freq_range:   The frequency range
        :type       freq_range:   [start_freq, end_freq]
        :param      sample_rate:  The sample rate
        :type       sample_rate:  float
        :param      options:      The options
        :type       options:      dictionary

        :returns:   ([freq], [abs(magnitude)], [phase angle])
        :rtype:     Tuple
        """
        logy = options.get('logy', False)
        num_steps = options.get('num_steps', 1000)
        max_freq = freq_range[-1]
        if freq_range[-1] >= (self.fs/2):
            max_freq = self.fs / 2
        frequencies = linspace(freq_range[0], max_freq, num_steps)

        results = ([], [], [])
        for frequency in frequencies:
            if frequency == 0:
                continue
            magnitude, phase_angle = self.evaluate_at_frequency(frequency, self.fs)
            magnitude = 20*math.log10(magnitude)
            results[0].append(frequency)
            results[1].append(magnitude)
            results[2].append(phase_angle)

        return results

    def reset(self, value=0):
        self.last_input = value
        self.last_output = value

    def calculate(self, input_sample):
        self.last_input = input_sample
        self.last_output = input_sample
        return input_sample

    def apply(self, data):
        self.reset(data[0])
        return [self.calculate(x) for x in data]

    def apply_zero_phase_filter(self, data):
        fwd = self.apply(data)
        rev = fwd[::-1]
        temp = self.apply(rev)
        return temp[::-1]

class FirstOrderIIRLowPass(FirstOrderIIR):
    def __init__(self, fc, fs):
        super().__init__(
            fc=fc,
            fs=fs
        )
    def calculate(self, input_sample):
        output = \
            self.alpha_lp*(input_sample + self.last_input) +\
            self.gamma*self.last_output
        self.last_input = input_sample
        self.last_output = output
        return output

    def evaluate_at_frequency(self, freq: float, sample_rate: float) -> Tuple:
        """
        evaluate the filter for a given frequency and sample rate

        :returns:   (abs(magnitude), phase angle)
        :rtype:     Tuple
        """
        # calculate constants, we can precompute sine and cosine terms
        # since we are evaluating for a single frequency
        theta = 2*math.pi * (freq/self.fs)
        theta_c = 2*math.pi* (self.fc / self.fs)
        cos1 = math.cos(theta)
        cos1c = math.cos(theta_c)
        sin1 = math.sin(theta)
        sin1c = math.sin(theta_c)
        
        num = (1 + cos1)*(1 - cos1c)
        dem = 2*(1-cos1*cos1c)
        magnitude = math.sqrt(num/dem)

        num = -1*(1+cos1c)*sin1
        dem = (1 + cos1)*sin1c
        safe_dem = APPROX_ZERO if dem == 0.0 else dem
        phase = math.atan(num/safe_dem) 
        # print(magnitude, phase)
        return (magnitude, phase)

class CombFilter:
    '''comb filter'''
    def __init__(self, **kwargs):
        '''init'''
        self.gain = kwargs.get('gain', 1.0)
        self.order = kwargs.get('order', 0)
        self._counter = 0
        # state buffer can be omitted in application
        # it is used for clarity sake, but can be substituted
        # by waiting until N samples have been taken, and
        # recording s[-N] for later use in a single state variable
        self._states = [0]*(self.order+1)
        self._output = 0

    #pylint: disable=too-many-locals
    def evaluate_at_frequency(self, freq: float, sample_rate: float) -> Tuple:
        """
        evaluate the comb for a given frequency and sample rate

        :returns:   (abs(magnitude), phase angle)
        :rtype:     Tuple
        """
        # calculate constants, we can precompute sine and cosine terms
        # since we are evaluating for a single frequency
        omega = 2*math.pi * (freq/sample_rate)
        cos = math.cos(omega*self.order)
        sin = math.sin(omega*self.order)
        
        if self.gain == 0:
            magnitude = 1.0
            phase = 0
        else: 
            magnitude = abs(math.sqrt((1+self.gain*cos)**2 + (self.gain*sin)**2))
            phase = math.atan((self.gain*sin)/(1+self.gain*cos))
    
        return (magnitude, phase)

    def reset(self, initial_condition=None):
        '''reset network'''
        if initial_condition is None:
            initial_condition = 0
        self._states = [initial_condition]*(self.order+1)
        self._counter = 0

    def update(self, sample):
        '''update the comb with a new sample,
        not sure if this is the correct to handle intial samples'''
        # quick n dirty delay line
        last_value = self._states.pop(1)
        self._states.append(sample)

        self._counter += 1
        if self._counter >= self.order:
            self._counter = self.order
        else:
            last_value = sample

        self._output = sample - last_value*self.gain

    @property
    def output(self):
        '''get the output of the comb'''
        return self._output

class DF2TBiquad:
    """
    Direct-Form-2 Transposed Biquad
    """
    def __init__(self, **kwargs):
        '''init'''
        #pylint: disable=C0103
        # Gains                  G[0], G[1], G[2]
        self.A = kwargs.get('A', [1.0, 0.0, 0.0])
        self.B = kwargs.get('B', [1.0, 0.0, 0.0])
        self._states = [0.0]*3
        self._output = 0.0

    #pylint: disable=too-many-locals
    def evaluate_at_frequency(self, freq: float, sample_rate: float) -> Tuple:
        """
        evaluate the filter for a given frequency and sample rate

        :returns:   (abs(magnitude), phase angle)
        :rtype:     Tuple
        """
        # calculate constants, we can precompute sine and cosine terms
        # since we are evaluating for a single frequency
        omega = 2*math.pi * (freq/sample_rate)
        cos1 = math.cos(omega)
        cos2 = math.cos(2*omega)
        sin1 = math.sin(omega)
        sin2 = math.sin(2*omega)

        # calculate numerator and denominator terms, implied that j has been factored out
        # from y terms such that it can be squared later
        numx = self.B[0] + self.B[1]*cos1 + self.B[2]*cos2
        numy = self.B[1]*sin1 - self.B[2]*sin2
        demx = 1.0/self.A[0] - self.A[1]*cos1 - self.A[2]*cos2
        demy = self.A[1]*sin1 - self.A[2]*sin2
    
        # calculate magnitude
        numhz = math.sqrt(numx**2 + numy**2)
        demhz = math.sqrt(demx**2 + demy**2)
        magnitude = abs(numhz/demhz)

        # calculate phase angle
        safe_numx = APPROX_ZERO if numx == 0.0 else numx
        safe_numy = APPROX_ZERO if numy == 0.0 else numy
        safe_demx = APPROX_ZERO if demx == 0.0 else demx
        safe_demy = APPROX_ZERO if demy == 0.0 else demy
        phase = math.atan(safe_numy/safe_numx) - math.atan(safe_demy/safe_demx)

        return (magnitude, phase)

    def update(self, sample):
        '''update biquad with new sample'''
        # states are in reverse,
        # i.e.
        #   S[2] = a0 * (sample - a1*S[1] - a2*S[0])
        #   S[1] = z^-1
        #   S[0] = z^-2

        # push new sample in, pop old one out
        # 3mult, 2add
        # --> 3rd mult is so we can have a0
        self._states.append(
            self.A[0]*\
            (sample - self.A[1]*self._states[-1]) -\
            self.A[2]*self._states[-2]
        )
        self._states.pop(1)
        # 3mult, 2add
        self._output = \
            self.B[0]*self.states[-1] + \
            self.B[1]*self.states[-2] + \
            self.B[2]*self.states[-3]


    @property
    def output(self):
        '''get output'''
        return self._output

    def reset(self, initial_conditions=None):
        '''reset biquad'''
        if initial_conditions is None:
            self._states = [0.0]*3
        else:
            self._states = initial_conditions[0:3]

class SAKNetwork:
    """
    "Swiss-Army-Knife" filter structure
    """
    def __init__(self, **kwargs):
        '''init'''
        self.comb = CombFilter(
            gain=kwargs.get('C', None),
            order=kwargs.get('N', None)
        )
        self.biquad = DF2TBiquad(
            A=kwargs.get('A', None),
            B=kwargs.get('B', None)
        )
        self._output = 0.0

    def evaluate_at_frequency(self, freq: float, sample_rate: float) -> Tuple:
        """
        evaluate the filter for a given frequency and sample rate

        :returns:   (abs(magnitude), phase angle)
        :rtype:     Tuple
        """
        responses = [
            self.comb.evaluate_at_frequency(freq, sample_rate),
            self.biquad.evaluate_at_frequency(freq, sample_rate)
        ]

        # calculate magnitude
        magnitude = responses[0][0] * responses[1][0]
        # calculate phase angle
        phase = responses[0][1] + responses[1][1]

        return (magnitude, phase)

    def get_frequency_response(self, freq_range, sample_rate: float, **options) -> Tuple:
        """
        Gets the frequency response for a given range of frequencies

        :param      freq_range:   The frequency range
        :type       freq_range:   [start_freq, end_freq]
        :param      sample_rate:  The sample rate
        :type       sample_rate:  float
        :param      options:      The options
        :type       options:      dictionary

        :returns:   ([freq], [abs(magnitude)], [phase angle])
        :rtype:     Tuple
        """
        logy = options.get('logy', False)
        num_steps = options.get('num_steps', 1000)
        max_freq = freq_range[-1]
        if freq_range[-1] >= (sample_rate/2):
            max_freq = sample_rate / 2
        frequencies = linspace(freq_range[0], max_freq, num_steps)

        results = ([], [], [])
        for frequency in frequencies:
            if frequency == 0:
                continue
            magnitude, phase_angle = self.evaluate_at_frequency(frequency, sample_rate)
            magnitude = 20*math.log10(magnitude)
            results[0].append(frequency)
            results[1].append(magnitude)
            results[2].append(phase_angle)

        return results


    def update(self, sample):
        '''update network with new sample'''
        self.comb.update(sample)
        self.biquad.update(self.comb.output)

    def reset(self):
        '''reset the state variables to zero'''
        self.comb.reset()
        self.biquad.reset()

class MovingAverager(SAKNetwork):
    pass

class Differencer(SAKNetwork):
    pass

class Integrator(SAKNetwork):
    pass

class LeakyIntegrator(SAKNetwork):
    pass

class DelayNetworkOrder1(SAKNetwork):
    pass

class GoertzelNetwork(SAKNetwork):
    pass

class RealOscillator(SAKNetwork):
    pass


# These Classes need A0 coefficients, and therefore a different
# difference equation
class DelayNetworkOrder2(SAKNetwork):
    pass




