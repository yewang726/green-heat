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
        self.cst_params()
        self.pv_params()
        self.wind_params()
        self.bat_params()
        self.TES_params()
        self.heater_params()
        self.finance_system_params()

    def cst_params(self):

        self.A_helio = 12.2*12.2 # m2, default heliostat size
        self.H_helio = 12.2 # heilisotat height
        self.c_helio = 127. # USD/m2
        self.c_helio_LB = 96. # USD/m2
        self.c_helio_UB = 140. # USD/m2
        self.c_helio_2030 = 75. # USD/m2

        self.c_site_cst = 16 # USD/m2 per area of heliostats        
        self.c_land=2.471 # USD/m2, 10,000 USD/acre

        # SAM:
        # Receiver Cost = Receiver Reference Cost x ( Receiver Area / Receiver Reference Area ) ^ Receiver Cost Scaling Exponent
        self.C_recv_ref = 103.e6 # USD, reference receiver cost
        self.A_recv_ref = 1571 # m2, reference receiver area
        self.f_recv_scale = 0.7 # receiver cost scaling exponent

        # SAM: 
        # Total Tower Cost = Fixed Tower Costs x e ^ ( Tower Cost Scaling Exponent x ( Tower Height - Receiver Height ÷ 2 + Heliostat Height ÷ 2 ) )
        self.C_tower_fixed = 3.e6 # USD, fixed tower cost
        self.f_tower_scale = 0.0113 # tower cost scaling exponent

        self.c_om_fixed_cst = 66 # USD/kW per year
        self.c_om_var_cst = 3.5 # USD/MWh per year
        

    def pv_params(self):
        self.c_pv=1122.73 # USD/kW
        self.c_om_fixed_pv=12.68 # USD/kW
        self.c_om_var_pv=0

    def wind_params(self):
        self.c_wind=1455.45 # USD/kW
        self.c_om_fixed_wind=18.65 # USD/kW
        self.c_om_var_wind=0

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


    def finance_system_params(self):
        self.r_conting = 0.07 # contingency cost
        self.r_disc_real = 0.064 # real discount rate
        self.r_EPC = 0.13 # ratio of EPC and owner cost to the direct cost, 13% default in SAM
        self.r_tax = 0.8*0.05 # sale tax, 80% of the direct cost with 5% tax rate in SAM
        self.t_life = 25 # int, life time of systems
        self.t_cons = 0 # construction time
    


  

