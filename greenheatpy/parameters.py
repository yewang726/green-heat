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
        #self.c_helio_LB = 96. # USD/m2
        #self.c_helio_UB = 140. # USD/m2
        #self.c_helio_2030 = 75. # USD/m2

        self.c_site_cst = 16 # USD/m2 per area of heliostats        
        self.c_land_cst=2.471 # USD/m2, 10,000 USD/acre

        # SAM:
        # Receiver Cost = Receiver Reference Cost x ( Receiver Area / Receiver Reference Area ) ^ Receiver Cost Scaling Exponent
        self.C_recv_ref = 103.e6 # USD, reference receiver cost
        self.A_recv_ref = 1571 # m2, reference receiver area
        self.f_recv_exp = 0.7 # receiver cost scaling exponent

        # SAM: 
        # Total Tower Cost = Fixed Tower Costs x e ^ ( Tower Cost Scaling Exponent x ( Tower Height - Receiver Height ÷ 2 + Heliostat Height ÷ 2 ) )
        self.C_tower_fix = 3.e6 # USD, fixed tower cost
        self.f_tower_exp = 0.0113 # tower cost scaling exponent

        self.c_om_cst_fix = 66 # USD/kW per year
        self.c_om_cst_var = 3.5 # USD/MWh per year

        self.r_EPC_owner=0.2 # rate of EPC and owner cost
        self.r_conting_cst = 0.1 # contingency rate
        self.t_constr_cst=3 # year of construction
        

    def pv_params(self):
        self.c_pv_system=1074.99 # USD/kW
        self.c_om_pv_fix=12.68 # USD/kW
        self.c_om_pv_var=0
        self.r_conting_pv=0.03 
        self.t_constr_pv=1


    def wind_params(self):
        self.c_wind_system=1462.16# USD/kW
        self.c_om_wind_fix=18.65 # USD/kW
        self.c_om_wind_var=0
        self.r_conting_wind=0.03 
        self.t_constr_wind=1

    def bat_params(self):
        # 0.82 round trip: https://www.eia.gov/todayinenergy/detail.php?id=46756 
        self.eff_rdtrip_bt=0.82
        self.c_bt_energy=250. # USD/kWh
        self.c_bt_power=230. # USD/kW
        self.t_life_bt =10 # heater lifetime
        self.c_replace_bt=self.c_bt_energy # replacement cost after lifetime

    def TES_params(self):
        self.eff_rdtrip_TES=0.99
        self.c_TES=22 # USD/kWh


    def heater_params(self):
        self.eff_heater=0.99
        self.c_heater=206. # USD/kW
        self.t_life_heater =10 # heater lifetime
        self.c_replace_heater=0.6*self.c_heater # replacement cost after lifetime


    def finance_system_params(self):
        #self.r_conting = 0.07 # contingency cost
        self.r_disc_real = 0.064 # real discount rate
        #self.r_EPC = 0.13 # ratio of EPC and owner cost to the direct cost, 13% default in SAM
        self.t_life = 25 # int, life time of systems
        #self.t_cons = 0 # construction time
    


  

