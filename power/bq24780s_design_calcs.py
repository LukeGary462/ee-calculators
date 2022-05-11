#!/usr/bin/env python
# python 3
#pylint: disable=
##    @file:    bq24780s_design_calcs.py
#     @name:    Luke Gary
#  @company:    <company>
#     @date:    2021/10/6
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
design calculations for BQ24780S Lithium-Ion battery charger IC
https://www.ti.com/document-viewer/BQ24780S/datasheet/application-and-implementation#SLUSBW02438
"""

class SW_MOSFET:
    def __init__(self, mpn, rdson, qgd, qgs, qg, vplt):
        self.mpn = mpn
        self.rdson = rdson
        self.gate_charge = qg
        self.gate_source_charge = qgs
        self.gate_drain_charge = qgd
        self.switching_charge = self.gate_drain_charge + (0.5*self.gate_source_charge)
        self.fom_top = self.rdson * self.gate_drain_charge
        self.fom_bot = self.rdson * self.gate_charge
        self.vplt = vplt

def calculate_mosfet_power_dissipation(**kwargs):
    '''calculate losses in switching fet and synchronous rectifier fet'''
    
    vin = kwargs.get('vin', 19.0)
    ''' https://biomeme.atlassian.net/wiki/spaces/THREE9/pages/520585291/Three9+Battery+Pack+Data+Flash+Image+V0.0.1 '''
    vout = kwargs.get('vout', 16.8)
    vregn = kwargs.get('vregn', 6.0)
    fet_top = kwargs.get('fet_top')
    fet_bot = kwargs.get('fet_bot')
    ''' https://biomeme.atlassian.net/wiki/spaces/THREE9/pages/520585291/Three9+Battery+Pack+Data+Flash+Image+V0.0.1 '''
    ichg = kwargs.get('ichg', 3.008)
    ''' 1MHz set in charge-controller.c charge option register 0 '''
    fs = kwargs.get('sw_freq', 1e6) 
    hsd_rdson = kwargs.get('hsd_rdson', 6)
    hsd_rdsoff = kwargs.get('hsd_rdsoff', 0.9)
    lsd_rdson = kwargs.get('lsd_rdson', 7.5)
    lsd_rdsoff = kwargs.get('lsd_rdsoff', 0.75)

    # calculate performance chars
    duty = vout/vin
    ion = (vregn - fet_top.vplt) / hsd_rdson
    ioff = fet_top.vplt / hsd_rdsoff
    ton_top = fet_top.switching_charge / ion
    toff_top = fet_top.switching_charge / ioff

    ptop = \
        (duty * ichg**2 * fet_top.rdson) + \
        0.5 * vin * ichg * (ton_top + toff_top) * fs

    # calculate power dissipation in synchronus rectification mode only
    pbot = \
        (1 - duty) * ichg**2 * fet_bot.rdson

    ptot = ptop + pbot

    print(f"Top FET power dissipation : {ptop:0.4f} Watts")
    print(f"Bot FET power dissipation : {pbot:0.4f} Watts")
    print(f"Converter Power dissipation at full charge current : {ptot:0.4f} Watts")

    if kwargs.get('print_all'):
        print(f'    duty        : {duty:0.4f} %')
        print(f'    ion         : {ion:0.4f} A')
        print(f'    ioff        : {ioff:0.4f} A')
        print(f'    ton_top     : {ton_top*1e6:0.4f} us')
        print(f'    toff_top    : {toff_top*1e6:0.4f} us')

def eval_fets():
    '''evaluate a few mosfets'''

    fets = [
        SW_MOSFET(
            mpn='(current design) NVTFS5C471NL',
            rdson=0.01,
            qgd=1.8e-9,
            qgs=2.6e-9,
            qg=5.5e-9,
            vplt=3.3
        ),
        SW_MOSFET(
            mpn='NVTFS5824NL',
            rdson=0.0225,
            qgd=4e-9,
            qgs=3e-9,
            qg=8.3e-9,
            vplt=3.25
        ),
        SW_MOSFET(
            mpn='NTTFS4929N',
            rdson=0.011,
            qgd=4.4e-9,
            qgs=2.8e-9,
            qg=8.8e-9,
            vplt=3.0,
        ),
        SW_MOSFET(
            mpn='NVTFS5C478NL',
            rdson=0.01665,
            qgd=1.2e-9,
            qgs=1.9e-9,
            qg=3.8e-9,
            vplt=3.6,
        ),
        SW_MOSFET(
            mpn='NTTFS4C13N',
            rdson=0.009333,
            qgd=3.7e-9,
            qgs=2.9e-9,
            qg=7.8e-9,
            vplt=3.6,
        )
    ]

    for fet in fets:
        print(f'\nEvaluating {fet.mpn} ... ')
        calculate_mosfet_power_dissipation(
            fet_top=fet,
            fet_bot=fet,
            print_all=True
        )

if __name__ == '__main__':
    eval_fets()