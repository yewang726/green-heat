import pandas as pd
import numpy as np
import os
from projdirs import datadir #load the path that contains the data files 
from PACKAGE.optimisation_green_heat import make_dzn_file, optimise
from PACKAGE.component_model import WindSource, SolarResource,pv_gen, wind_gen,solcast_weather, SolarResource_solcast, WindSource_solcast
from PACKAGE.get_location import get_location

import matplotlib.pyplot as plt

def AUD2USD(value):
    return(0.746 * value)

def master(location, RM, t_storage, P_load_des=500e3, casedir=None, verbose=False):
    '''
    Arguments:
        location   (str)  : site location
        RM         (float): renewable multiple, the total size of the renewable energy collection system (e.g. PV+Wind) to the load
        t_storage  (float): storage hour (h)
        P_load_des (float): system load design power (W)

    Returns:


    '''

    if not os.path.exists(casedir):
        os.makedirs(casedir)

    ### Get wind and solar data for the designated location

    Lat,Lon = get_location(location)

    if not os.path.exists(casedir+'/WindSource.csv'):
        WindSource(Lat, Lon, casedir)
    if not os.path.exists(casedir+'/SolarSource.epw'):
        SolarResource(Lat,Lon, casedir)
    #solcast_weather(Newman)
    #SolarResource_solcast()
    #WindSource_solcast()


    ### Get SAM reference system outputs
    pv_ref_capa = 1e3 #(kW)
    pv_ref_out = pv_gen(pv_ref_capa, casedir)

    wind_ref_capa = 200e3 #(kW)
    wind_ref_out = wind_gen(wind_ref_capa, casedir)

    ### Set the inputs for plant optimisation and run the optimisation
    #   These inputs are used by make_dzn_file function to create an input text file called hydrogen_plant_data.dzn. 
    ETA_heater=0.99
    P_heater=P_load_des/ETA_heater

    simparams = dict(DT = 1.,# [h] time steps
                     RM = RM, # renewable multiple
                     t_storage = t_storage, # [h] storage hour
                     BAT_ETA_in = 0.95,   # charging efficiency of battery
                     BAT_ETA_out = 0.95,  # discharg efficiency of battery
                     P_heater = P_heater, # [kW] heater designed power
                     ETA_heater = ETA_heater, # heater efficiency
                     C_PV = 1122.73,  # [USD/kW] unit cost of PV
                     C_Wind = 1455.45, # [USD/kW] unit cost of W
                     C_BAT_energy = 196.76, # [USD/kWh] unit cost of battery energy storage
                     C_BAT_power = 405.56 ,  # [USD/kW] unit cost of battery power capacpity
                     C_heater = 206., # [USD/kW] unit cost of heater
                     PV_ref_capa = pv_ref_capa,    #capacity of reference PV plant (kW)
                     PV_ref_out = pv_ref_out,           #power output from reference PV plant (kW)
                     Wind_ref_capa = wind_ref_capa,      #capacity of reference wind farm (kW)
                     Wind_ref_out = wind_ref_out,        #power output from the reference wind farm (kW)
                     L = [P_load_des for i in range(len(pv_ref_out))],  #[kW] load profile timeseries
                     casedir = casedir)  # directory of the minizinc input data file 

    #run the optimisation function and get the results in a dictionary:
    results = optimise(simparams)

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
    P_st_in=results["P_st_in"]
    P_st_out=results["P_st_out"]
    P_ele=results["P_ele"]
    P_heat=results["P_heat"]
    bat_e_stored=results["bat_e_stored"]
    load=results["L"]


    summary=np.array([
            ['RM',RM, '-'],
            ['t_storage', t_storage, 'h'],
            ['CF', CF, '-'],
            ['CAPEX', CAPEX, 'M.USD'],
            ['r_pv', r_pv, '-'],
            ['pv_max', pv_max, 'MW'],
            ['wind_max', wind_max, 'MW'],
            ['bat_capa',bat_capa, 'MWh'],
            ['bat_pmax',bat_pmax, 'MW']
    ])


    np.savetxt(casedir+'/summary_%.1f_%.1f.csv'%(RM, t_storage), summary, fmt='%s', delimiter=',')
    
    if verbose:
        np.savetxt(casedir+'/pv_out.csv', pv_out, fmt='%.4f', delimiter=',')
        np.savetxt(casedir+'/wind_out.csv', wind_out, fmt='%.4f', delimiter=',')
        np.savetxt(casedir+'/P_curt.csv', P_curt, fmt='%.4f', delimiter=',')
        np.savetxt(casedir+'/P_st_in.csv', P_st_in, fmt='%.4f', delimiter=',')
        np.savetxt(casedir+'/P_st_out.csv', P_st_out, fmt='%.4f', delimiter=',')
        np.savetxt(casedir+'/P_ele.csv', P_ele, fmt='%.4f', delimiter=',')
        np.savetxt(casedir+'/P_heat.csv', P_heat, fmt='%.4f', delimiter=',')
        np.savetxt(casedir+'/bat_e_stored.csv', bat_e_stored, fmt='%.4f', delimiter=',')
        np.savetxt(casedir+'/load.csv', load, fmt='%.4f', delimiter=',')


        time=np.arange(len(pv_out))
        plt.plot(time, pv_out, label='pv out')
        plt.plot(time, wind_out, label='wind out')
        plt.plot(time, P_ele, label='P_ele')
        plt.plot(time, P_curt, label='P_curt')
        plt.plot(time, P_st_in, label='P_st_in')
        plt.plot(time, P_st_out, label='P_st_out')
        plt.plot(time, load, label='load')
        plt.legend()
        plt.show()
        plt.close()

        '''
        pv_out=np.loadtxt('pv_out.csv', delimiter=',')
        wind_out=np.loadtxt('wind_out.csv',delimiter=',')
        P_ele=np.loadtxt('P_ele.csv',delimiter=',')
        P_curt=np.loadtxt('P_curt.csv', delimiter=',')
        P_st_in=np.loadtxt('P_st_in.csv', delimiter=',')
        P_st_out=np.loadtxt('P_st_out.csv', delimiter=',')

        print(np.max(P_curt))

        # check
        pv_wind_direct=P_ele-P_st_out
        check=(pv_out+ wind_out - P_curt - pv_wind_direct - P_st_in)
        print(np.sum(check))
        '''

if __name__=='__main__':
    location='Newman'
    SH=np.arange(0, 20, 1)
    RM=np.arange(1, 5, 0.5)

    for rm in RM:
        for sh in SH:
            casedir='./results/%s'%location
            res_fn=casedir+'/summary_%.1f_%.1f.csv'%(rm, sh)
            if not os.path.exists(res_fn):
                master(location=location, RM=rm, t_storage=sh, P_load_des=500e3, casedir=casedir, verbose=False)
            print('RM', rm, 'SH', sh, 'Done')




