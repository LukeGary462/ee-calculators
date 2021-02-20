#!/usr/bin/env python
# python 3
##    @file:    goertzel.py
#     @name:    Luke Gary
#  @company:    <company>
#     @date:    2021/2/18
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
import numpy as np

class Goertzel:
    """
    This class describes a goertzel filter.
    """
    def __init__(self):
        self.states = [0] * 3
        self.k = 0
        self.omega = 0
        self.coeff = 0
        self.count = 0
        self.block_size = 0

    @staticmethod
    def calculate_nominal_buffer_size(freq_target, freq_sample, discr_hz, max_samples=10000):
        '''calculate smallest Block size to get freq discrimintaion (discr_hz)'''
        block_size = max_samples
        for temp_block in range(1, max_samples):
            bin_size_hz = (freq_sample/temp_block)
            if bin_size_hz < discr_hz:
                block_size = temp_block
                break
        k = 0.5 + (block_size*freq_target)/freq_sample
        omega = 2*np.pi/block_size*k
        coeff = 2*np.cos(omega)
        settling_time_ms = ((1/freq_sample)*block_size)*1e3
        update_rate_hz = (1/((1/freq_sample)*block_size))
        return {
            'k': k,
            'w': omega,
            'a': coeff,
            'block_size': block_size,
            'settling_time_ms': settling_time_ms,
            'update_rate_hz': update_rate_hz
        }

    def initialize(self, freq_target, freq_sample, block_size):
        ''' init filter'''
        self.block_size = block_size
        self.k = int(0.5 + (block_size*freq_target)/freq_sample)
        self.omega = 2*np.pi/self.block_size*self.k
        self.coeff = 2*np.cos(self.omega)
        settling_time_ms = ((1/freq_sample)*self.block_size)*1e3
        update_rate_hz = (1/((1/freq_sample)*self.block_size))
        bin_width = freq_sample/self.block_size
        return {
            'k': self.k,
            'w': self.omega,
            'a': self.coeff,
            'block_size': self.block_size,
            'settling_time_ms': settling_time_ms,
            'update_rate_hz': update_rate_hz,
            'bin_width': bin_width
        }

    def reset(self):
        ''' reset state variables'''
        self.states = [0] * 3
        self.count = 0

    def update(self, sample, realtime=False):
        '''update the network'''
        self.states[0] = self.coeff*self.states[1]-self.states[2]+sample
        self.states[2] = self.states[1]
        self.states[1] = self.states[0]
        self.count += 1
        mag_sq = 0
        if realtime or (self.count >= self.block_size):
            mag_sq = self.states[1]**2 \
                +self.states[2]**2 \
                -(self.states[1]*self.states[2]*self.coeff)
        if self.count >= self.block_size:
            self.count = 0
            self.reset()
        return np.sqrt(mag_sq)

    @property
    def power(self):
        '''get magnitude of current state'''
        return  self.states[1]**2 +\
                self.states[2]**2 -\
                (self.states[1]*self.states[2]*self.coeff)
