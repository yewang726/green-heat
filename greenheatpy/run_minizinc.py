# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 10:28:44 2022 @author: Ahmad Mojiri
Modified on 18 Jun 2022 by Ye Wang for Green Heat models
"""

from greenheatpy.projdirs import optdir
import numpy as np
from subprocess import check_output

import platform


def run_minizinc(model_name, dzn_fn, casedir=None):
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



    if platform.system()=='Windows':
        mzdir = r'C:\\Program Files\\MiniZinc\\'
        output = str(check_output([mzdir + 'minizinc', "--soln-sep", '""',
                                   "--search-complete-msg", '""', "--solver",
                                   "COIN-BC", optdir + model_name+ ".mzn",
                                   dzn_fn]))
    elif platform.system()=='Linux':
        output = str(check_output(['minizinc', "--soln-sep", '""',
                                   "--search-complete-msg", '""', "--solver",
                                   "COIN-BC", optdir + model_name+ ".mzn",
                                   dzn_fn]))

    
    output = output.replace('[','').replace(']','').split('!')

    results = output[1].split(';')   
    results = list(filter(None, results))
    
    RESULTS = {}
    for x in results:
        RESULTS[x.split('=')[0]]=np.array((x.split('=')[1]).split(',')).astype(float)        
    
    return(  RESULTS  )



