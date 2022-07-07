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
        

    def pv_wind_battery_heat_outputs(self, results, casedir, LCOH):

        CAPEX=results["CAPEX"][0]/1e6 # M.USD
        CF=results["CF"][0]
        RM=results["RM"][0]
        t_storage=results["t_storage"][0]
        r_pv=results["r_pv"][0]
        pv_max=results["pv_max"][0]/1.e3 # MW
        wind_max=results["wind_max"][0]/1.e3 # MW
        bat_capa=results["bat_capa"][0]/1.e3 # MWh
        bat_pmax=results["bat_pmax"][0]/1.e3 # MW
        pv_out=results["pv_out"]
        wind_out=results["wind_out"]
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
                ['CAPEX', CAPEX, 'M.USD'],
                ['r_pv', r_pv, '-'],
                ['pv_max', pv_max, 'MW'],
                ['wind_max', wind_max, 'MW'],
                ['bat_capa',bat_capa, 'MWh'],
                ['bat_pmax',bat_pmax, 'MW']
        ])

        np.savetxt(casedir+'/summary_%.3f_%.2f.csv'%(RM, t_storage), summary, fmt='%s', delimiter=',')
        
        if self.verbose:
            np.savetxt(casedir+'/pv_out.csv', pv_out, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/wind_out.csv', wind_out, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_curt.csv', P_curt, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_bat_in.csv', P_bat_in, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_bat_out.csv', P_bat_out, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_ele.csv', P_ele, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_heat.csv', P_heat, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/bat_e_stored.csv', bat_e_stored, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/load.csv', load, fmt='%.4f', delimiter=',')


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




    def pv_battery_heat_outputs(self, results, casedir, LCOH):

        CAPEX=results["CAPEX"][0]/1e6 # M.USD
        CF=results["CF"][0]
        RM=results["RM"][0]
        t_storage=results["t_storage"][0]
        pv_max=results["pv_max"][0]/1.e3 # MW
        bat_capa=results["bat_capa"][0]/1.e3 # MWh
        bat_pmax=results["bat_pmax"][0]/1.e3 # MW
        pv_out=results["pv_out"]
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
                ['CAPEX', CAPEX, 'M.USD'],
                ['pv_max', pv_max, 'MW'],
                ['bat_capa',bat_capa, 'MWh'],
                ['bat_pmax',bat_pmax, 'MW']
        ])

        np.savetxt(casedir+'/summary_%.3f_%.2f.csv'%(RM, t_storage), summary, fmt='%s', delimiter=',')
        
        if self.verbose:
            np.savetxt(casedir+'/pv_out.csv', pv_out, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_curt.csv', P_curt, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_bat_in.csv', P_bat_in, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_bat_out.csv', P_bat_out, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_ele.csv', P_ele, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_heat.csv', P_heat, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/bat_e_stored.csv', bat_e_stored, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/load.csv', load, fmt='%.4f', delimiter=',')



    def wind_battery_heat_outputs(self, results, casedir, LCOH):

        CAPEX=results["CAPEX"][0]/1e6 # M.USD
        CF=results["CF"][0]
        RM=results["RM"][0]
        t_storage=results["t_storage"][0]
        wind_max=results["wind_max"][0]/1.e3 # MW
        bat_capa=results["bat_capa"][0]/1.e3 # MWh
        bat_pmax=results["bat_pmax"][0]/1.e3 # MW
        wind_out=results["wind_out"]
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
                ['CAPEX', CAPEX, 'M.USD'],
                ['wind_max', wind_max, 'MW'],
                ['bat_capa',bat_capa, 'MWh'],
                ['bat_pmax',bat_pmax, 'MW']
        ])

        np.savetxt(casedir+'/summary_%.3f_%.2f.csv'%(RM, t_storage), summary, fmt='%s', delimiter=',')
        
        if self.verbose:
            np.savetxt(casedir+'/wind_out.csv', wind_out, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_curt.csv', P_curt, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_bat_in.csv', P_bat_in, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_bat_out.csv', P_bat_out, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_ele.csv', P_ele, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/P_heat.csv', P_heat, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/bat_e_stored.csv', bat_e_stored, fmt='%.4f', delimiter=',')
            np.savetxt(casedir+'/load.csv', load, fmt='%.4f', delimiter=',')


    def pv_wind_TES_heat_outputs(self, results, casedir, LCOH):

        CAPEX=results["CAPEX"][0]/1e6 # M.USD
        CF=results["CF"][0]
        RM=results["RM"][0]
        t_storage=results["t_storage"][0]
        r_pv=results["r_pv"][0]
        pv_max=results["pv_max"][0]/1.e3 # MW
        wind_max=results["wind_max"][0]/1.e3 # MW
        TES_capa=results["TES_capa"][0]/1.e3 # MWh
        TES_pmax=results["TES_pmax"][0]/1.e3 # MW
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
                ['CAPEX', CAPEX, 'M.USD'],
                ['r_pv', r_pv, '-'],
                ['pv_max', pv_max, 'MW'],
                ['wind_max', wind_max, 'MW'],
                ['TES_capa',TES_capa, 'MWh'],
                ['TES_pmax',TES_pmax, 'MW'],
                ['P_heater',P_heater, 'MW']
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


    def CST_TES_heat_outputs(self, results, casedir, SM, H_recv, D_recv, H_tower, n_helios, A_land, LCOH):

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
                ['TES_pmax',TES_pmax, 'MW']
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
  

