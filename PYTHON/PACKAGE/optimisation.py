# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 10:28:44 2022

@author: Ahmad Mojiri
"""
from projdirs import optdir
import numpy as np
# import pdb

def make_dzn_file(DT, ETA_EL, BAT_ETA_in, BAT_ETA_out,
                  C_PV, C_W, C_EL, C_HS, C_BAT_energy, C_BAT_power,  CF,
                  PV_ref_capa, PV_ref_out, Wind_ref_capa, Wind_ref_out, L):

    # pdb.set_trace()    
    string = """
    N = %i;
    
    DT = %.3f;      %% time difference between sample points (hr)
    
    ETA_EL = %.3f;  %% conversion factor of the electrolyser
    BAT_ETA_in = %.3f;   %%charging efficiency of electrochemical battery
    BAT_ETA_out = %.3f;  %%discharging efficiency of electrochemical battery 
    
    C_PV = %.3f;    %% unit cost of PV ($/kW)
    C_W =  %.3f;    %% unit cost of Wind farm ($/kW)
    C_EL =  %.3f;    %% unit cost of electrolyser ($/kW)
    C_HS = %.3f;    %% unit cost of hydrogen storage ($/kgH)
    C_BAT_energy = %.3f;   %% unit cost of electrochemical battery energy ($/kWh)
    C_BAT_power = %.3f;   %% unit cost of electrochemical battery power ($/kWh)
    
    R_CAPA = %.3f;       %% reserved hydrogen for lowered capcaity factor
    
    pv_ref_capa = %.3f;       %%the capacity of the reference PV plant (W)
    
    %% Power output time series from reference PV plant (W)
    pv_ref_out = %s;                                  
     
     
    wind_ref_capa = %.3f;  %% the capacity of the refernce wind plant (W)
    
    %% power output time series from the reference wind plant (W)
    wind_ref_out = %s;  
    
    %% load timeseries (kgH/s)                             
    L = %s;                              
    """ %(len(L), DT, ETA_EL, BAT_ETA_in, BAT_ETA_out,
      C_PV, C_W, C_EL, C_HS, C_BAT_energy, C_BAT_power, 
      (1-CF)*sum(L)*DT, PV_ref_capa, str(PV_ref_out), Wind_ref_capa,
      str(Wind_ref_out), str(L))

    with open(optdir + "hydrogen_plant_data.dzn", "w") as text_file:
        text_file.write(string)
        
        
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
    make_dzn_file(**simparams)
    mzdir = r'C:\\Program Files\\MiniZinc\\'
    from subprocess import check_output
    output = str(check_output([mzdir + 'minizinc', "--soln-sep", '""',
                               "--search-complete-msg", '""', "--solver",
                               "COIN-BC", optdir + "hydrogen_plant.mzn",
                               optdir + "hydrogen_plant_data.dzn"]))
    
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

