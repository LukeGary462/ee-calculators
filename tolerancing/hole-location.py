#!/usr/bin/env python
# python 3
##    @file:    hole-location.py
#     @name:    Luke Gary
#  @company:    <company>
#     @date:    2021/8/12
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
GD&T Hole location tolerancing
"""

import argparse


class Hole:
    """
    This class describes a hole.
    """
    def __init__(self, **kwargs):
        """init"""
        self.diameter   = kwargs.get('dia', 1.0)
        self.mmc        = kwargs.get('mmc', )


if __name__ == '__main__':

