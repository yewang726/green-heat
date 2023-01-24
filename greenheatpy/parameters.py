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
        self.F_future_cost=0.2 #e.g. nominal_2030=(1-0.2)*nominal, nominal_2050=(1-0.2)*nominal_2030
        self.cst_params()
        self.pv_params()
        self.wind_params()
        self.bat_params()
        self.PHES_params()
        self.TES_params()
        self.heater_params()
        self.finance_system_params()

  

    def cst_params(self):

        self.A_helio = 12.2*12.2 # m2, default heliostat size
        self.H_helio = 12.2 # heilisotat height
        self.c_helio = 127. # USD/m2
        self.c_helio_2030 = 75. # G3P3
        self.c_helio_2050 = 50. # HelioCon target TODO check 
        #self.c_helio_LB = 96. # USD/m2
        #self.c_helio_UB = 140. # USD/m2
        #self.c_helio_2030 = 75. # USD/m2

        self.c_site_cst = 16 # USD/m2 per area of heliostats      
        self.c_site_cst_2030 = 10
        self.c_site_cst_2050 = self.c_site_cst_2030*(1.-self.F_future_cost) # TODO future cost is not sure 
          
        self.c_land_cst=2.471 # USD/m2, 10,000 USD/acre
        self.c_land_cst_2030 = self.c_land_cst
        self.c_land_cst_2050 = self.c_land_cst

        # SAM:
        # Receiver Cost = Receiver Reference Cost x ( Receiver Area / Receiver Reference Area ) ^ Receiver Cost Scaling Exponent
        self.C_recv_ref = 103.e6 # USD, reference receiver cost
        self.C_recv_ref_2030 = self.C_recv_ref  * (1.-self.F_future_cost)    # TODO
        self.C_recv_ref_2050 = self.C_recv_ref_2030 * (1.-self.F_future_cost)   

        self.A_recv_ref = 1571 # m2, reference receiver area
        self.f_recv_exp = 0.7 # receiver cost scaling exponent

        # SAM: 
        # Total Tower Cost = Fixed Tower Costs x e ^ ( Tower Cost Scaling Exponent x ( Tower Height - Receiver Height ÷ 2 + Heliostat Height ÷ 2 ) )
        self.C_tower_fix = 3.e6 # USD, fixed tower cost
        self.C_tower_fix_2030 = self.C_tower_fix  * (1.-self.F_future_cost)    #TODO
        self.C_tower_fix_2050 = self.C_tower_fix_2030 * (1.-self.F_future_cost)  

        self.f_tower_exp = 0.0113 # tower cost scaling exponent

        self.c_om_cst_fix = 66 # USD/kW per year
        self.c_om_cst_var = 3.5 # USD/MWh per year

        self.r_EPC_owner=0.2 # rate of EPC and owner cost
        self.r_conting_cst = 0.1 # contingency rate
        self.t_constr_cst=3 # year of construction



    def pv_params(self):
        self.c_pv_system=1074.99 # USD/kW # 2021-2022 GenCost report
        self.c_pv_system_2030=755.70
        self.c_pv_system_2050=480.424

        self.c_om_pv_fix=12.68 # USD/kW
        self.c_om_pv_var=0
        self.r_conting_pv=0.03 
        self.t_constr_pv=1


    def wind_params(self):
        self.c_wind_system=1462.16# USD/kW 2021-2022 GenCost report
        self.c_wind_system_2030=1415.16
        self.c_wind_system_2050=1363.69

        self.c_om_wind_fix=18.65 # USD/kW
        self.c_om_wind_var=0
        self.r_conting_wind=0.03 
        self.t_constr_wind=1

    def bat_params(self):
        # 0.82 round trip: https://www.eia.gov/todayinenergy/detail.php?id=46756 
        self.eff_rdtrip_bt=0.82
        self.c_bt_energy=250. # USD/kWh (Fig5, NREL, https://www.nrel.gov/docs/fy21osti/79236.pdf)
        self.c_bt_energy_2030=150.
        self.c_bt_energy_2050=100.

        self.c_bt_power=230. # USD/kW
        self.c_bt_power_2030=199.
        self.c_bt_power_2050=180.
 
        self.t_life_bt =10 # heater lifetime
        self.c_replace_bt=self.c_bt_energy # replacement cost after lifetime

    def PHES_params(self):
        self.eff_rdtrip_PHES=0.79
        self.c_PHES_energy=50. # USD/kWh https://energystorage.shinyapps.io/LCOSApp/
        self.c_PHES_energy_2030=self.c_PHES_energy * (1.-self.F_future_cost)    #TODO future cost of PHES is unsure
        self.c_PHES_energy_2050=self.c_PHES_energy_2030 * (1.-self.F_future_cost)   


        self.c_PHES_power=1100. # USD/kW
        self.c_PHES_power_2030=self.c_PHES_power * (1.-self.F_future_cost) 
        self.c_PHES_power_2050=self.c_PHES_power_2030 * (1.-self.F_future_cost)   

        self.c_om_PHES_fix=20. # USD/kW
        self.c_om_PHES_var=0.0004 #USD/kWh


    def TES_params(self):
        self.eff_rdtrip_TES=0.99
        self.c_TES=22 # USD/kWh TODO
        self.c_TES_2030=self.c_TES * (1.-self.F_future_cost)  
        self.c_TES_2050=self.c_TES_2030 * (1.-self.F_future_cost)   



    def heater_params(self):
        self.eff_heater=0.99
        self.c_heater=206. # USD/kW TODO
        self.c_heater_2030=self.c_heater  * (1.-self.F_future_cost)   
        self.c_heater_2050=self.c_heater_2030 * (1.-self.F_future_cost)   

        self.t_life_heater =10 # heater lifetime
        self.c_replace_heater=0.6*self.c_heater # replacement cost after lifetime


    def finance_system_params(self):
        self.r_disc_real = 0.064 # real discount rate
        self.t_life = 25 # int, life time of systems
    


def CST_SL_OM(A_helios):
    '''
    OM cost of CST using Sargent & Lundy (2003) analysis
    https://www.nrel.gov/docs/fy04osti/34440.pdf

    '''
    c_labour=2.11549e-9*A_helios**2-0.01438705*A_helios+65188.593 # USD/person
    c_labour=max(c_labour, 42000.)
    #num_labour_helio=int(1.7596e-12*A_helios**2+9.3236*A_helios*1e-6+5.7523)+1
    num_labour_helio=int(1.50830474e-5*A_helios+2.3784455)+1
    num_labour_others=int(15*0.25)+1 # include receiver, TES (assumed it is 1/4 of the total 15 staff required for a whole plant)
    C_labour=(num_labour_helio+num_labour_others)*c_labour

    C_service=(7.923561e-5*A_helios+155.637032)*1000. # USD

    c_water=0.32 #USD/m3
    u_water=0.022*A_helios # water ussage m3
    C_water=c_water*u_water

    c_material=0.25 #USD/m2, for heliostats wear and tear (parts and material) 
    C_material=c_material*A_helios

    #c_equipment=(1.0535e-7*A_helios+0.09432)/5. # USD/m2, Unit cost of heliostat maintenance equipment per heliostat per year
    c_equipment=(1.1023381e-7*A_helios+0.08467133184)/5.
    C_equipment=c_equipment*A_helios

    CI_2003=402
    CI_2022=628.22
    F_update=CI_2022/CI_2003

    OM=(C_labour+C_service+C_water+C_material+C_equipment)*F_update
    #print(F_update)
    #print(c_labour)
    #print(num_labour_helio, num_labour_others, C_labour)
    #print(C_water, C_material, C_equipment)
    return OM

if __name__=='__main__':
    A_helios=81400
    OM=CST_SL_OM(A_helios)
    print(OM, abs(OM-1136023)<5)
  
    A_helios=2606000
    OM=CST_SL_OM(A_helios)
    print(OM, abs(OM-4370947)<5)

