# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 10:28:44 2022 @author: Ahmad Mojiri
Modified on 18 Jun 2022 by Ye Wang for Green Heat models
"""
from projdirs import optdir
import numpy as np

import platform

def make_dzn_file(DT, RM, t_storage, BAT_ETA_in, BAT_ETA_out, P_heater, ETA_heater, 
                  C_PV, C_Wind, C_BAT_energy, C_BAT_power, C_heater,
                  PV_ref_capa, PV_ref_out, Wind_ref_capa, Wind_ref_out, L, casedir=None, obj=None):

    string="""
N = %i;

DT = %.2f;      %% time difference between sample points (s)

RM = %.1f;  %% renewable multiple
t_storage = %.1f;   %% storage hour (h)

BAT_ETA_in = %.2f;   %%charging efficiency of electrochemical battery
BAT_ETA_out = %.2f;  %%discharging efficiency of electrochemical battery 

P_heater = %.1f;    %% design power of the heater (W)
ETA_heater = %.4f;  %% efficiency of the heater

C_PV = %.4f;    %% unit cost of PV ($/W)
C_Wind =  %.4f;    %% unit cost of Wind farm ($/W)
C_BAT_energy = %.6f;   %% unit cost of electrochemical battery energy ($/W.s)
C_BAT_power = %.6f;   %% unit cost of electrochemical battery power ($/W)
C_heater = %.6f;   %% unit cost of heater ($/W)

pv_ref_capa = %.4f;       %%the capacity of the reference PV plant (W)

%% Power output time series from reference PV plant (W)
pv_ref_out = %s;                                  
 
wind_ref_capa = %.4f;  %% the capacity of the refernce wind plant (W)

%% power output time series from the reference wind plant (W)
wind_ref_out = %s;  

%% load timeseries                          
L = %s;                              
"""%(len(L), DT, RM, t_storage, BAT_ETA_in, BAT_ETA_out,
      P_heater, ETA_heater,
      C_PV, C_Wind, C_BAT_energy, C_BAT_power, C_heater,
      PV_ref_capa, str(PV_ref_out), Wind_ref_capa,
      str(Wind_ref_out), str(L)) 


    if obj=='CF':
        model_name='pv_wind_battery_heat_obj-CF'

    if casedir==None:
        dzn_fn=optdir +"%s_data.dzn"%model_name
    else:
        dzn_fn=casedir+"/%s_data.dzn"%model_name

    with open(dzn_fn, "w") as text_file:
        text_file.write(string)

    return dzn_fn
        
        
#####################################################################
def optimise(simparams):
    """
    Parameters
    ----------
    simparams : a dictionary including the following parameters:
        DT, ETA_PV, ETA_EL, C_PV, C_W, C_E, C_HS, CF, pv_ref_capa,
                  W, pv_ref_out, L

    Returns
    -------
    a list of outputs including the optimal values for CAPEX, p-pv, p_w, p_e,
    e_hs

    """
    dzn_fn=make_dzn_file(**simparams)
    from subprocess import check_output

    obj=simparams['obj']
    if obj=='CF':
        model_name='pv_wind_battery_heat_obj-CF'

    if platform.system()=='Windows':
        mzdir = r'C:\\Program Files\\MiniZinc\\'
        output = str(check_output([mzdir + 'minizinc', "--soln-sep", '""',
                                   "--search-complete-msg", '""', "--solver",
                                   "COIN-BC", optdir + ".mzn"%model_name,
                                   dzn_fn]))
    elif platform.system()=='Linux':
        output = str(check_output(['minizinc', "--soln-sep", '""',
                                   "--search-complete-msg", '""', "--solver",
                                   "COIN-BC", optdir + "%s.mzn"%model_name,
                                   dzn_fn]))

    
    output = output.replace('[','').replace(']','').split('!')
    for string in output:
        if 'CAPEX' in string:
            results = string.split(';')
    
    results = list(filter(None, results))
    
    RESULTS = {}
    for x in results:
        RESULTS[x.split('=')[0]]=np.array((x.split('=')[1]).split(',')).astype(float)        
    
    return(  RESULTS  )


######################################################################

