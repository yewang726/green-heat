# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 10:28:44 2022

@author: Ahmad Mojiri
"""
from projdirs import optdir
import numpy as np


def make_dzn_file(DT, ETA_EL, BAT_ETA_in, BAT_ETA_out,
                  C_PV, C_W, C_EL, C_HS, C_BAT, CF, PV_ref_capa,
                  PV_ref_out, Wind_ref_capa, Wind_ref_out, L):

    
    string = """
N = %i;

DT = %.2f;      %% time difference between sample points (s)

ETA_EL = %.2f;  %% conversion factor of the electrolyser (kgH/s/W)
BAT_ETA_in = %.2f;   %%charging efficiency of electrochemical battery
BAT_ETA_out = %.2f;  %%discharging efficiency of electrochemical battery 

C_PV = %.4f;    %% unit cost of PV ($/W)
C_W =  %.4f;    %% unit cost of Wind farm ($/W)
C_EL =  %.4f;    %% unit cost of electrolyser ($/W)
C_HS = %.4f;    %% unit cost of hydrogen storage ($/kgH)
C_BAT = %.6f;   %% unit cost of electrochemical battery ($/W.s)

R_CAPA = %.4f;       %% reserved hydrogen for lowered capcaity factor

pv_ref_capa = %.4f;       %%the capacity of the reference PV plant (W)

%% Power output time series from reference PV plant (W)
pv_ref_out = %s;                                  
 
 
wind_ref_capa = %.4f;  %% the capacity of the refernce wind plant (W)

%% power output time series from the reference wind plant (W)
wind_ref_out = %s;  

%% load timeseries (kgH/s)                             
L = %s;                              
""" %(len(L), DT, ETA_EL, BAT_ETA_in, BAT_ETA_out,
      C_PV, C_W, C_EL, C_HS, C_BAT, 
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

