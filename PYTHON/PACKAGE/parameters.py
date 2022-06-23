# -*- coding: utf-8 -*-
"""
Created on 23 Jun 2022 by Ye Wang for Green Heat models
"""

import numpy as np

class Parameters:

    def __init__(self):
        '''
        set the default value of parameters (cost and performance)  
        '''
        self.pv_params()
        self.wind_params()
        self.bat_params()
        self.TES_params()
        self.heater_params()

    def pv_params(self):
        self.c_pv=1122.73 # USD/kW

    def wind_params(self):
        self.c_wind=1455.45 # USD/kW

    def bat_params(self):
        self.eta_bat_in=0.95
        self.eta_bat_out=0.95
        self.c_bat_energy=196.76 # USD/kWh
        self.c_bat_power=405.56 # USD/kW


    def TES_params(self):
        self.eta_TES_in=0.95
        self.eta_TES_out=0.95
        self.c_TES=22 # USD/kWh

    def heater_params(self):
        self.eta_heater=0.99
        self.c_heater=206. # USD/kW


  

