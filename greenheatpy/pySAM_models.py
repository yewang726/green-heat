# -*- coding: utf-8 -*-
"""
Originally created on Fri May 6 12:46:54 2022 by Ahmad Mojiri

Modified by Ye Wang
"""

from greenheatpy.projdirs import datadir

import numpy as np
import json, io, requests
import PySAM.Pvwattsv8 as PVWatts, Windpower
import PySAM.TcsmoltenSalt as CSP
import platform


def pv_gen(capacity, wea_fn=None):
    """
    Arguments:
        capacity (float): system capacity (kW)
        wea_fn     (str): directory of the weather data file for the SAM PV model
                the default 'None' will load the weather file in the 'data' directory
    Return:
        output    (list): energy production (kW) by the PV system in time series in a year 
    
    """
    module = PVWatts.new()

    if platform.system()=='Windows':
        json_fn=datadir+'\json_pvWatts\default_pvwattsv8.json' 
    elif platform.system()=='Linux':
        json_fn=datadir+'/json_pvWatts/default_pvwattsv8.json'   
  
    with open(json_fn, 'r') as f:
        data = json.load(f)
    f.close()
    for k,v in data.items():
        if k != "number_inputs":
            module.value(k, v)

    if wea_fn==None:
        module.value('solar_resource_file', datadir+'/SolarSource.csv')
    else:
        module.value('solar_resource_file', wea_fn)

        
    module.SystemDesign.system_capacity = capacity
    module.execute()
    output = np.array(module.Outputs.gen)
    output=output.tolist()

    return output


def wind_gen(capacity, wea_fn=None):
    """
    Arguments:
        capacity (float): system capacity (kW)
        wea_fn     (str): directory of the weather data file for the SAM Wind model
                the default 'None' will load the weather file in the 'data' directory
    Return:
        output    (list): energy production (kW) by the Wind system in time series in a year 
 
    """
    module = Windpower.new()

    if platform.system()=='Windows':
        json_fn=datadir+'\json_windpower\default_windpower.json' 
    elif platform.system()=='Linux':
        json_fn=datadir+'/json_windpower/default_windpower.json'   
    
    with open(json_fn, 'r') as f:
        data = json.load(f)
    f.close()

    for k,v in data.items():
        if k != "number_inputs":
            module.value(k, v)

    if wea_fn==None:
        module.value('wind_resource_filename', datadir+'/WindSource.csv')
    else:
        module.value('wind_resource_filename', wea_fn)

    module.value('system_capacity', capacity)
    
    module.execute()
    output = np.array(module.Outputs.gen)
    output=output.tolist()

    return output



def cst_gen(Q_des_th, SM, wea_fn=None):

    """
    Arguments:
        Q_des_th (float): system design thermal power (kW)
        SM       (float): solar multiple
        wea_fn     (str): directory of the weather data file for the SAM solartower model
                the default 'None' will load the weather file in the 'data' directory
    Return:
        Q_rcv_out (list): thermal output from the receiver (kW_th) in time series in a year 
        H_recv   (float): the optimal receiver height designed by SAM (m)
        D_recv   (float): the optimal receiver diameter designed by SAM (m)
        H_tower  (float): the optimal tower height designed by SAM (m)
        n_helios (float): the optimal number of heliostats designed by SAM (-)
        A_land   (float): the total land area of the optimal field layout designed by SAM (m2)
 
    """
    module = CSP.new()

    if platform.system()=='Windows':
        json_fn=datadir+'\json_cst\SAM-CSP-molten-salt_tcsmolten_salt.json' 
    elif platform.system()=='Linux':
        #json_fn=datadir+'/json_cst/SAM-CSP-molten-salt_tcsmolten_salt.json'   
        json_fn=datadir+'/json_cst/SAM-CSP-molten-salt_tcsmolten_salt.json'  
    
    with open(json_fn, 'r') as f:
        data = json.load(f)
    f.close()

    for k,v in data.items():
        if k != "number_inputs":
            module.value(k, v)

    module.value('field_model_type', 0) # SAM will optimise the field, tower and receiver size 
    module.value('f_rec_min', 1e-6) # minimal receiver turndown fraction
    module.value('solarm', SM) # solar multiple
    module.value('tshours', 100) # because this model only takes the receiver output, a very large storage is set to ignor impact from SAM control 

    if wea_fn==None:
        module.value('solar_resource_file', datadir+'/SolarSource.csv')
    else:
        module.value('solar_resource_file', wea_fn)

    P_pb_name=Q_des_th*0.412/1000. # 0.412 is the default PB efficiency, and convert to MW
    module.value('P_ref', P_pb_name) # this is capacity of electricity, 

    module.execute()

    H_recv=module.TowerAndReceiver.rec_height #Receiver height [m]
    D_recv=module.TowerAndReceiver.D_rec #The overall outer diameter of the receiver [m]
    H_tower=module.TowerAndReceiver.h_tower # Tower height [m]
    n_helios=module.HeliostatField.N_hel #Number of heliostats
    A_land=module.Outputs.csp_pt_cost_total_land_area*4046.86 # Total land area [m2] (converted [acre] to m2)

    #eta_field=module.Outputs.eta_field # field optical efficiency
    eta_recv=np.array(module.Outputs.eta_therm) # receiver thermal efficiency
    Q_recv_in=np.array(module.Outputs.q_dot_rec_inc) # incident thermal power on the receiver [MW_th]

    Q_recv_out=Q_recv_in*eta_recv*1000. # kW_th 
    #np.savetxt('sam_Q_recv_in.csv', Q_recv_in, fmt='%.4f', delimiter=',')
    #np.savetxt('sam_eta_recv.csv', eta_recv, fmt='%.6f', delimiter=',')
    Q_rcv_out=Q_recv_out.tolist()

    return Q_rcv_out, H_recv, D_recv, H_tower, n_helios, A_land




