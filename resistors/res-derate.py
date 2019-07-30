#!/usr/bin/env python
# python 3
##  @file:                  res-derate.py
#   @par:
#   @author:                Luke Gary
#   @company:               REE
#   @date:                  2018/11/26
#   @brief:
#   @verbatim:

################################################################
# @copyright
#   Copyright 2018 Rye Effects Research as an  unpublished work.
#   All Rights Reserved.
#
# @license The information contained herein is confidential
#   property of Rye Effects Research. The user, copying, transfer or
#   disclosure of such information is prohibited except
#   by express written agreement with Rye Effects Research.
################################################################
#/
import numpy as np
import math
import argparse

BOLTZMAN = 1.38065e-23

def get_options():
    parser = argparse.ArgumentParser(description='calculate various resistor parameter deratings')
    parser.add_argument('-')
    return parser.parse_args()
