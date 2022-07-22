# -*- coding: utf-8 -*-
"""
Created on 23 Jun 2022 by Ye Wang for Green Heat models
"""

import numpy as np
import matplotlib.pyplot as plt

class Outputs:

    def __init__(self, verbose=False):
        '''
        set the default value of parameters (cost and performance)  
        '''
        self.verbose=verbose
        
    def pv_wind_battery_heat_outputs(self, results, casedir, LCOH, location, solar_data_fn, wind_data_fn, epy, OM_total, C_cap, CAPEX, C_pv, C_wind, C_bat, C_heater,  C_replc_heater_NPV, C_replc_bt_NPV, C_replace_NPV, r_disc_real, t_life, t_cons, eta_storage):

        #CAPEX=results["CAPEX"][0]/1e6 # M.USD
        CF=results["CF"][0]
        RM=results["RM"][0]
        t_storage=results["t_storage"][0]
        r_pv=results["r_pv"][0]
        pv_max=results["pv_max"][0]/1.e3 # MW
        wind_max=results["wind_max"][0]/1.e3 # MW
        bat_capa=results["bat_capa"][0]/1.e3 # MWh
        bat_pmax=results["bat_pmax"][0]/1.e3 # MW
        P_heater=results["P_heater"][0]/1.e3 # MW
        pv_out=results["pv_out"]
        wind_out=results["wind_out"]
        pv_wind_direct=results["pv_wind_direct"]
        P_curt=results["P_curt"]
        P_bat_in=results["P_bat_in"]
        P_bat_out=results["P_bat_out"]
        P_ele=results["P_ele"]
        P_heat=results["P_heat"]
        bat_e_stored=results["bat_e_stored"]
        load=results["L"]

        summary=np.array([
                ['RM',RM, '-'],
                ['t_storage', t_storage, 'h'],
                ['LCOH', LCOH, 'USD/MWh_th'],
                ['CF', CF, '-'],
                ['r_pv', r_pv, '-'],
                ['pv_max', pv_max, 'MW'],
                ['wind_max', wind_max, 'MW'],
                ['P_heater',P_heater, 'MW'],
                ['bat_capa',bat_capa, 'MWh'],
                ['bat_pmax',bat_pmax, 'MW'],
                ['storage in/out efficiency', eta_storage, '-'],
                ['EPY', epy, 'MWh'],
                ['C_cap_tot', C_cap/1e6, 'M.USD'],
                ['OM_tot', OM_total/1e6, 'M.USD'],
                ['C_equipment', CAPEX/1e6, 'M.USD'],
                ['C_pv', C_pv/1e6, 'M.USD'],            
                ['C_wind', C_wind/1e6, 'M.USD'],  
                ['C_bat', C_bat/1e6, 'M.USD'],  
                ['C_heater', C_heater/1e6, 'M.USD'],  
                ['C_replace_heater_NPV', C_replc_heater_NPV/1e6, 'M.USD'],  
                ['C_replace_bt_NPV', C_replc_bt_NPV/1e6, 'M.USD'],  
                ['C_replace_NPV', C_replace_NPV/1e6, 'M.USD'],  
                ['r_real_discount', r_disc_real, '-'],
                ['t_construction', t_cons, 'year'],
                ['t_life', t_life, 'year'],
                ['location',location, '-'],
                ['solar_data',solar_data_fn, '-'],
                ['wind_data',wind_data_fn, '-']                
        ])

        np.savetxt(casedir+'/summary_%.3f_%.2f.csv'%(RM, t_storage), summary, fmt='%s', delimiter=',')
        
        if self.verbose:
            np.savetxt(casedir+'/pv_out.csv', pv_out, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/wind_out.csv', wind_out, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/pv_wind_direct.csv', pv_wind_direct, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_curt.csv', P_curt, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_bat_in.csv', P_bat_in, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_bat_out.csv', P_bat_out, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_ele.csv', P_ele, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_heat.csv', P_heat, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/bat_e_stored.csv', bat_e_stored, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/load.csv', load, fmt='%.4f', delimiter=',')

            '''
            time=np.arange(len(pv_out))
            plt.plot(time, pv_out, label='pv out')
            plt.plot(time, wind_out, label='wind out')
            plt.plot(time, P_ele, label='P_ele')
            plt.plot(time, P_curt, label='P_curt')
            plt.plot(time, P_bat_in, label='P_bat_in')
            plt.plot(time, P_bat_out, label='P_bat_out')
            plt.plot(time, load, label='load')
            plt.legend()
            plt.show()
            plt.close()
            '''


    def pv_wind_TES_heat_outputs(self, results, casedir, LCOH, location, solar_data_fn, wind_data_fn, epy, OM_total, C_cap, CAPEX, C_pv, C_wind, C_TES, C_heater, C_replace_NPV, r_disc_real, t_life, t_cons, eta_storage):

        #CAPEX=results["CAPEX"][0]/1e6 # M.USD
        CF=results["CF"][0]
        RM=results["RM"][0]
        t_storage=results["t_storage"][0]
        r_pv=results["r_pv"][0]
        pv_max=results["pv_max"][0]/1.e3 # MW
        wind_max=results["wind_max"][0]/1.e3 # MW
        TES_capa=results["TES_capa"][0]/1.e3 # MWh
        #TES_pmax=results["TES_pmax"][0]/1.e3 # MW
        P_heater=results["P_heater"][0]/1.e3 # MW
        pv_out=results["pv_out"]
        wind_out=results["wind_out"]
        P_curt=results["P_curt"]
        P_heater_in=results["P_heater_in"]
        P_heater_out=results["P_heater_out"]
        P_heat_direct=results["P_heat_direct"]
        P_TES_in=results["P_TES_in"]
        P_TES_out=results["P_TES_out"]
        P_heat=results["P_heat"]
        TES_e_stored=results["TES_e_stored"]
        load=results["L"]


        summary=np.array([
                ['RM',RM, '-'],
                ['t_storage', t_storage, 'h'],
                ['LCOH', LCOH, 'USD/MWh_th'],
                ['CF', CF, '-'],
                ['r_pv', r_pv, '-'],
                ['pv_max', pv_max, 'MW'],
                ['wind_max', wind_max, 'MW'],
                ['P_heater',P_heater, 'MW'],
                ['TES_capa',TES_capa, 'MWh'],
                #['TES_pmax',TES_pmax, 'MW'],
                ['storage in/out efficiency', eta_storage, '-'],
                ['EPY', epy, 'MWh'],
                ['C_cap_tot', C_cap/1e6, 'M.USD'],
                ['OM_tot', OM_total/1e6, 'M.USD'],
                ['C_equipment', CAPEX/1e6, 'M.USD'],
                ['C_pv', C_pv/1e6, 'M.USD'],            
                ['C_wind', C_wind/1e6, 'M.USD'],  
                ['C_TES', C_TES/1e6, 'M.USD'],  
                ['C_heater', C_heater/1e6, 'M.USD'],  
                ['C_replace_heater_NPV', C_replace_NPV/1e6, 'M.USD'],  
                ['r_real_discount', r_disc_real, '-'],
                ['t_construction', t_cons, 'year'],
                ['t_life', t_life, 'year'],
                ['location',location, '-'],
                ['solar_data',solar_data_fn, '-'],
                ['wind_data',wind_data_fn, '-']   
        ])

        np.savetxt(casedir+'/summary_%.3f_%.2f.csv'%(RM, t_storage), summary, fmt='%s', delimiter=',')
        
        if self.verbose:
            np.savetxt(casedir+'/pv_out.csv', pv_out, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/wind_out.csv', wind_out, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_curt.csv', P_curt, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_heater_in.csv', P_heater_in, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_heater_out.csv', P_heater_out, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_heat_direct.csv', P_heat_direct, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_TES_in.csv', P_TES_in, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_TES_out.csv', P_TES_out, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_heat.csv', P_heat, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/TES_e_stored.csv', TES_e_stored, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/load.csv', load, fmt='%.4f', delimiter=',')


    def CST_TES_heat_outputs(self, results, casedir, SM, H_recv, D_recv, H_tower, n_helios, A_land, LCOH, location, solar_data_fn, epy, OM_total, C_cap, C_indirect, C_direct, CAPEX, C_recv, C_tower, C_field, C_site, C_TES, C_land, r_disc_real, t_life, t_cons, eta_storage):

        CF=results["CF"][0]
        t_storage=results["t_storage"][0]
        TES_capa=results["TES_capa"][0]/1.e3 # MWh
        TES_pmax=results["TES_pmax"][0]/1.e3 # MW
        P_recv_out=results["P_recv_out"]
        P_curt=results["P_curt"]
        P_direct=results["P_direct"]
        P_TES_in=results["P_TES_in"]
        P_TES_out=results["P_TES_out"]
        P_heat=results["P_heat"]
        TES_e_stored=results["TES_e_stored"]
        load=results["L"]


        summary=np.array([
                ['SM',SM, '-'],
                ['t_storage', t_storage, 'h'],
                ['LCOH', LCOH, 'USD/MWh_th'],
                ['CF', CF, '-'],
                ['H_recv', H_recv, 'm'],
                ['D_recv', D_recv, 'm'],
                ['H_tower', H_tower, 'm'],
                ['n_helios', n_helios, '-'],
                ['A_land', A_land, 'm2'],
                ['TES_capa',TES_capa, 'MWh'],
                ['TES_pmax',TES_pmax, 'MW'],
                ['storage in/out efficiency', eta_storage, '-'],
                ['EPY', epy, 'MWh'],
                ['C_cap_tot', C_cap/1e6, 'M.USD'],
                ['OM_tot', OM_total/1e6, 'M.USD'],
                ['C_recv', C_recv/1e6, 'M.USD'],
                ['C_tower', C_tower/1e6, 'M.USD'],
                ['C_field', C_field/1e6, 'M.USD'],
                ['C_site', C_site/1e6, 'M.USD'],
                ['C_TES', C_TES/1e6, 'M.USD'],
                ['C_land', C_land/1e6, 'M.USD'],
                ['C_equipment', CAPEX/1e6, 'M.USD'],
                ['C_direct', C_direct/1e6, 'M.USD'],
                ['C_indirect', C_indirect/1e6, 'USD'],
                ['r_real_discount', r_disc_real, '-'],
                ['t_construction', t_cons, 'year'],
                ['t_life', t_life, 'year'],
                ['location',location, '-'],
                ['solar_data',solar_data_fn, '-']
        ])

        np.savetxt(casedir+'/summary_%.3f_%.2f.csv'%(SM, t_storage), summary, fmt='%s', delimiter=',')
        
        if self.verbose:
            np.savetxt(casedir+'/P_recv_out.csv', P_recv_out, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_curt.csv', P_curt, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_direct.csv', P_direct, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_TES_in.csv', P_TES_in, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_TES_out.csv', P_TES_out, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_heat.csv', P_heat, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/TES_e_stored.csv', TES_e_stored, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/load.csv', load, fmt='%.4f', delimiter=',')
  

