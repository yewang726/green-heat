# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 18:54:47 2022

@author: Ahmad Mojiri
"""

from projdirs import optdir
import numpy as np
import pandas as pd



def prep_results_to_print(results,simparams):
    
    RESULTS =    {'Capacity Factor': results['CF'],
                  'CAPEX [USD]':results['CAPEX'][0],
                'PV Rated Power[kW]': results['pv_max'][0],
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
                'Load [kg/s]':results['LOAD'][0]
                 }
    output = str(RESULTS).replace(', ',',\n ').replace('{', '').replace('}', '').replace("'",'').replace(',','')   
    return(output)
    
    
    