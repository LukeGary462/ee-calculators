##  @file:          johnson.py
#   @par:
#   @author:        Luke Gary
#   @company:       Biomeme, Inc
#   @date:          2019/6/6
#   @brief:
#   @verbatim:

################################################################
# @copyright
# Copyright 2019 [Biomeme, Inc] as an  unpublished work.
# All Rights Reserved.
#
# @license The information contained herein is confidential
# property of [Biomeme, Inc]. The user, copying, transfer or
# disclosure of such information is prohibited except
# by express written agreement with [Biomeme, Inc].
################################################################
#/

import math

BOLTZMAN = 1.38065e-23
def tempC_to_tempK(tempCelsius):
    return 273.15 + tempCelsius

def resistor_vrms(temperatureKelvin, resistance, bandwidth):
    return math.sqrt((4 * BOLTZMAN)*temperatureKelvin*resistance*bandwidth)

def vrms_to_vpp(vrms):
    return 6.6 * vrms;

def johnson(res, temp=25.0, bw=1e6):
  #convert to list of numbers
  if isinstance(res, int):
    res = float(res)
    res = [res]
  elif isinstance(res, float):
    res = [res]

  rmss = []
  for r in res:
    uVrms = resistor_vrms(tempC_to_tempK(float(temp)), float(r), float(bw)) * 1e6
    uVpp = vrms_to_vpp(uVrms)
    rmss.append(uVrms)
    print("R:{0:.2f} Ohms, BW:{1} Hz".format(r, bw))
    print(" uVrms:{0:.4f}, uVpp:{1:.4f}".format(
      uVrms, uVpp))
  total = 0.0
  for v in rmss:
    total += math.pow(v,2.0)
  total = math.sqrt(total)
  print("Total RMS noise is {0:.4f} uVrms".format(total))
  print("Total VPP noise is {0:.4f} uVpp".format(vrms_to_vpp(total)))