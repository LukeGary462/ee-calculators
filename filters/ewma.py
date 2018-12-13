#!/usr/bin/env python
# python 3
##  @file:                  EWMA.py
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

import math

##
## @brief      Class for 0-6th order cascade exponential weighted moving average
##
class EWMA:
    def __init__(self, coeff, initialValue):
        ##
        ## ewma3 states for coefficient optimization
        ##
        self.last_ewma3 = [0.0,0.0,0.0]

        ##
        ## ewma6 states for coefficient optimization
        ##
        self.last_ewma6 = [0.0,0.0,0.0,0.0,0.0,0.0]

        ##
        ## default coefficients to 1.0 so the order can be from 0 - 6
        ## since cascade elements will pass input signal to output with a=1
        ##
        self.coeff = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

        for c in range(0, len(coeff)):
            if(c >= len(self.coeff)):
                print(f'EWMA Coefficients Length Mismatch! len(coeff) = {len(coeff)}, max is 6')
                break;
            self.coeff[c] = coeff[c]
        ##
        ## realtime filter states
        ##
        self.states = [0,0,0,0,0,0,0]
        self.states[0] = initialValue
        self.states[1] = initialValue
        self.states[2] = initialValue
        self.states[3] = initialValue
        self.states[4] = initialValue
        self.states[5] = initialValue
        self.states[6] = initialValue

    def preload(self, value):
        self.states[0] = value
        self.states[1] = value
        self.states[2] = value
        self.states[3] = value
        self.states[4] = value
        self.states[5] = value
        self.states[6] = value

    ##
    ## @brief      calculate single EWMA element
    ##
    ## @param      self   The object
    ## @param      alpha  filter coefficient
    ## @param      this   current input sample
    ## @param      last   last output sample from this stage (feedback)
    ##
    ## @return     EWMA result
    ##
    def ewma(self, alpha, this, last):
        return (float(alpha)*float(this)) + ((1.0-float(alpha))*float(last))

    ##
    ## @brief      calculate 6th order cascade ewma
    ##
    ## @param      self        The object
    ## @param      inputValue  Raw input sample
    ##
    ## @return     output of 6th cascade element
    ##
    def calculate(self, inputValue):
        result = 0.0
        self.states[0] = float(inputValue)
        self.states[1] = self.ewma(float(self.coeff[0]), self.states[0], self.states[1])
        self.states[2] = self.ewma(float(self.coeff[1]), self.states[1], self.states[2])
        self.states[3] = self.ewma(float(self.coeff[2]), self.states[2], self.states[3])
        self.states[4] = self.ewma(float(self.coeff[3]), self.states[3], self.states[4])
        self.states[5] = self.ewma(float(self.coeff[4]), self.states[4], self.states[5])
        self.states[6] = self.ewma(float(self.coeff[5]), self.states[5], self.states[6])
        return self.states[6]

    def get_last_output(self):
        return self.states[6]

    def model_ewma3_preload(self, v):
        self.last_ewma3[0] = v
        self.last_ewma3[1] = v
        self.last_ewma3[2] = v

    ##
    ## @brief      ewma 3rd order for IIR Model Fitting via SciPy Optimize
    ##
    ## @param      self  The object
    ## @param      y0    The input value
    ## @param      a     coeff a
    ## @param      b     coeff b
    ## @param      c     coeff c
    ##
    ## @return     IIR output
    ##
    def model_ewma3(self, y0, a, b, c):
        y1 = self.ewma(a, y0, self.last_ewma3[0])
        y2 = self.ewma(b, y1, self.last_ewma3[1])
        y3 = self.ewma(c, y2, self.last_ewma3[2])
        self.last_ewma3[0] = y1
        self.last_ewma3[1] = y2
        self.last_ewma3[2] = y3
        return y3

    def model_ewma6_preload(self, v):
        self.last_ewma6[0] = v
        self.last_ewma6[1] = v
        self.last_ewma6[2] = v
        self.last_ewma6[3] = v
        self.last_ewma6[4] = v
        self.last_ewma6[5] = v

    ##
    ## @brief      ewma 6th order for IIR Model Fitting via SciPy Optimize
    ##
    ## @param      self  The object
    ## @param      y0    The Input Value
    ## @param      a     coeff a
    ## @param      b     coeff b
    ## @param      c     coeff c
    ## @param      d     coeff d
    ## @param      e     coeff e
    ## @param      f     coeff f
    ##
    ## @return     { description_of_the_return_value }
    ##
    def model_ewma6(self, y0, a, b, c, d, e, f):
        y1 = self.ewma(a, y0, self.last_ewma3[0])
        y2 = self.ewma(b, y1, self.last_ewma3[1])
        y3 = self.ewma(c, y2, self.last_ewma3[2])
        y4 = self.ewma(d, y3, self.last_ewma3[3])
        y5 = self.ewma(e, y4, self.last_ewma3[4])
        y6 = self.ewma(f, y5, self.last_ewma3[5])
        self.last_ewma6[0] = y1
        self.last_ewma6[1] = y2
        self.last_ewma6[2] = y3
        self.last_ewma6[3] = y4
        self.last_ewma6[4] = y5
        self.last_ewma6[5] = y6
        return y6

    def get_cutoff(self, Fs=1.0):
        x = [1.0,1.0,1.0,1.0,1.0,1.0]
        try:
            x[0] = (Fs/2*math.pi)*math.acos(1.0 - (math.pow(self.coeff[0], 2)/(2.0*(1.0 - self.coeff[0]))))
        except:
            print("filter tap not initialized")
        try:
            x[1] = (Fs/2*math.pi)*math.acos(1.0 - (math.pow(self.coeff[1], 2)/(2.0*(1.0 - self.coeff[1]))))
        except:
            print("filter tap not initialized")
        try:
            x[2] = (Fs/2*math.pi)*math.acos(1.0 - (math.pow(self.coeff[2], 2)/(2.0*(1.0 - self.coeff[2]))))
        except:
            print("filter tap not initialized")
        try:
            x[3] = (Fs/2*math.pi)*math.acos(1.0 - (math.pow(self.coeff[3], 2)/(2.0*(1.0 - self.coeff[3]))))
        except:
            print("filter tap not initialized")
        try:
            x[4] = (Fs/2*math.pi)*math.acos(1.0 - (math.pow(self.coeff[4], 2)/(2.0*(1.0 - self.coeff[4]))))
        except:
            print("filter tap not initialized")
        try:
            x[5] = (Fs/2*math.pi)*math.acos(1.0 - (math.pow(self.coeff[5], 2)/(2.0*(1.0 - self.coeff[5]))))
        except:
            print("filter tap not initialized")

        return x


def test():
    import numpy as np
    import matplotlib.pyplot as plt

    alpha   = 0.1523347
    beta    = 0.0547115
    gamma   = 0.059647154
    coeff = [alpha, beta, gamma]
    filt = EWMA(coeff, 0)
    print(filt.get_cutoff(Fs=33.333))

    # test func model for optimization
    t = np.arange(0,100,0.1)
    inputs = []
    for i in range(0, len(t)):
        if i < len(t)/2:
            v = -1.0
        else:
            v = 1.0
        inputs.append(v)

    outputs = []
    realishOutputs = []
    filt.model_ewma3_preload(inputs[0])
    filt.preload(inputs[0])
    for i in range(0, len(inputs)):
        outputs.append(filt.model_ewma3(inputs[i], *coeff))
        realishOutputs.append(filt.calculate(inputs[i]))
    plt.figure()
    plt.plot(inputs,label='in')
    plt.plot(outputs,label='optimout')
    plt.plot(realishOutputs,label='realish', linestyle=':')
    plt.legend(loc='best')
    plt.show()

if __name__ == '__main__':
    test()
