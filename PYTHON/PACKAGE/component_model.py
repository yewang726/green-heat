# -*- coding: utf-8 -*-
"""
Created on Fri May  6 12:46:54 2022

@author: Ahmad Mojiri
"""
from projdirs import datadir

import numpy as np
import json
import PySAM.Pvwattsv8 as PVWatts


def pv_gen(capacity):
    """
    Parameters
    ----------
    capacity in W

    Returns system powr generated in W for each hour in a year
    
    """
    pv = PVWatts.new()
    
    dir = datadir + '\SAM INPUTS\SOLAR\\'
    file_name = 'pv_plant_pvwattsv8'
    module = pv
    
    with open(dir + file_name + ".json", 'r') as file:
        data = json.load(file)
        for k,v in data.items():
            if k != "number_inputs":
                module.value(k, v)
    
    module.SystemDesign.system_capacity = capacity/1000
    pv.execute()
    output = np.array(pv.Outputs.gen)*1000
    return(output.tolist())