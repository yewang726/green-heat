# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 18:54:47 2022

@author: Ahmad Mojiri
"""

from projdirs import optdir, datadir
import numpy as np
import pandas as pd
import platform



def read_data_for_plotting(results):
        data_to_plot = {}
        (KEYS,VALUES) = (list(results.keys()),list(results.values()))
        for (k,v) in zip(KEYS,VALUES):
            if len(v)>1:
                data_to_plot[k]=v[0:int(results['N'][0])]
        return(pd.DataFrame(data_to_plot))



def prep_results_to_print(results,simparams):
    
    RESULTS =  {'Capacity Factor [%]': results['CF'],
                'CAPEX [USD]':results['CAPEX'][0],
                'PV Rated Power [kW]': results['pv_max'][0],
                'Wind Rated Power [kW]': results['wind_max'][0],
                'Electrolyser rated Power [kW]': results['el_max'][0],
                'UG H2 Capacity [kgH2]': results['ug_storage_capa'][0],
                'Pipe Storage Capacity [kgH2]': results['pipe_storage_capa'][0],
                'Battery Energy Capacity [kWh]': results['bat_e_capa'][0],
                'Battery Power Capacity [kW]': results['bat_p_max'][0],
                'PV Cost [USD]': results['pv_max'][0]*simparams['C_PV'],
                'Wind Cost [USD]': results['wind_max'][0]*simparams['C_WIND'],
                'Electrolyser Cost [USD]': results['el_max'][0]*simparams['C_EL'],
                'UG Storage Cost [USD]': results['ug_storage_capa'][0]*results['C_UG_STORAGE'],
                'Pipe Storage Cost [USD]':results['pipe_storage_capa'][0]*simparams['C_PIPE_STORAGE'],
                'Battery Cost [USD]': results['bat_p_max'][0]*simparams['C_BAT_ENERGY'],
                'Load [kg/s]':results['LOAD'][0],
                'UG Storage Unit Price [USD/kgH2]':results['C_UG_STORAGE']
                 }
    return(RESULTS)





def prep_results_to_plot(results,simparams,Location):
    del results['CF']
    del results['C_UG_STORAGE']
    
    path = datadir/'SAM_INPUTS'/'WEATHER_DATA'/'weather_data_{}.csv'.format(Location)
        
    weather_data = pd.read_csv(path,skiprows=2)
    
    
    data_plot = read_data_for_plotting(results)
    
    beam = weather_data['DNI'].tolist()
    G_H = weather_data['GHI']
    wind_speed = weather_data['Wind Speed']
    
    water_rate = 15 #L/kgH2  range: 15-20 L/kgH2
    c_water = 5 # $/m3
    
    data_plot['beam'] = beam
    data_plot['t'] = np.arange(0,results['N'])
    data_plot['time'] =pd.to_datetime('2021-01-01') + pd.to_timedelta(data_plot.t, 'h')
    data_plot.drop('t',axis=1,inplace=True)
    data_plot['G_H'] = G_H
    data_plot['wind_speed'] = wind_speed   
    return(data_plot)
    
    




def crf(rate,years):
    return(  (rate*(1+rate)**years) / ((1+rate)**years-1)  )




def LCOH2(RESULTS, data_to_plot, i, life,
          pv_fom, wind_fom, elec_fom,
          pv_vom, wind_vom, elec_vom):
    
    H2_total = data_to_plot.LOAD.sum()*RESULTS['Capacity Factor [%]']/100
    i = i/100
    
    CFR = i*(1+i)**life / ( (1+i)**life-1  )
    
    pv_FOM = pv_fom * RESULTS['PV Rated Power [kW]'] / H2_total     
    wind_FOM = wind_fom * RESULTS['Wind Rated Power [kW]'] / H2_total
    elec_FOM = elec_fom * RESULTS['Electrolyser rated Power [kW]'] / H2_total
    
    pv_CAPEX = RESULTS['PV Cost [USD]'] * CFR / H2_total
    wind_CAPEX = RESULTS['Wind Cost [USD]'] * CFR / H2_total
    elec_CAPEX = RESULTS['Electrolyser Cost [USD]'] * CFR / H2_total
    
    storage_CAPEX = (  RESULTS['UG Storage Cost [USD]'] + 
                       RESULTS['Pipe Storage Cost [USD]'] ) * CFR / H2_total
    
    LCOH2_items = pd.DataFrame({
                              'Capex PV': [pv_CAPEX],
                              'Capex Wind': [wind_CAPEX],
                              'Capex Electrolyser': [elec_CAPEX],
                              'CAPEX Storage': [storage_CAPEX],
                              'FOM PV': [pv_FOM],
                              'FOM Wind': [wind_FOM],
                              'FOM Electrolyser': [elec_FOM],
                              'VOM PV': [pv_vom],
                              'VOM Wind': [wind_vom],
                              'VOM Electrlyser': [elec_vom]
                              
                              })
                  
    return(LCOH2_items)

