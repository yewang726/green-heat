import pandas as pd
import numpy as np
import os
from projdirs import datadir #load the path that contains the data files 
from PACKAGE.optimisation_green_heat import optimise
from PACKAGE.component_model import WindSource, SolarResource,pv_gen, wind_gen,solcast_weather, SolarResource_solcast, WindSource_solcast
from PACKAGE.get_location import get_location
from PACKAGE.parameters import Parameters
from PACKAGE.outputs import Outputs
from PACKAGE.gen_minizinc_input_data import GenDZN


def AUD2USD(value):
    return(0.746 * value)

def master(model_name, location, RM, t_storage, P_load_des=500e3, r_pv=None, casedir=None, verbose=False):
    '''
    Arguments:
        model_name (str)  : minizic model name
        location   (str)  : site location
        RM         (float): renewable multiple, the total size of the renewable energy collection system (e.g. PV+Wind) to the load
        t_storage  (float): storage hour (h)
        P_load_des (float): system load design power (W)
        casedir    (str)  : the case directory, if the default None is kept, it will load/save data in 'datadir'
        verbose    (bool) : to save and plot the time series results or not

    Returns:

    '''
    if not os.path.exists(casedir):
        os.makedirs(casedir)

    Lat,Lon = get_location(location)

    if 'pv' in model_name:
        # Get solar data
        if not os.path.exists(casedir+'/SolarSource.epw'):
            SolarResource(Lat,Lon, casedir)
        # Get SAM reference system outputs
        pv_ref_capa = 1e3 #(kW)
        pv_ref_out = pv_gen(pv_ref_capa, casedir)        


    if 'wind' in model_name:
        # Get wind data
        if not os.path.exists(casedir+'/WindSource.csv'):
            WindSource(Lat, Lon, casedir)
        # Get SAM reference system outputs
        wind_ref_capa = 200e3 #(kW)
        wind_ref_out = wind_gen(wind_ref_capa, casedir)

    #solcast_weather(Newman)
    #SolarResource_solcast()
    #WindSource_solcast()


    # Set the inputs for plant optimisation and run the optimisation
    # These inputs are used by make_dzn_file function to create an input text file called hydrogen_plant_data.dzn. 
    pm=Parameters()
    if model_name=='pv_wind_battery_heat':
        P_heater=P_load_des/pm.eta_heater
        simparams = dict(DT = 1.,# [h] time steps
                         RM = RM, # renewable multiple
                         t_storage = t_storage, # [h] storage hour
                         BAT_ETA_in = pm.eta_bat_in,   # charging efficiency of battery
                         BAT_ETA_out = pm.eta_bat_out,  # discharg efficiency of battery
                         P_heater = P_heater, # [kW] heater designed power
                         ETA_heater = pm.eta_heater, # heater efficiency
                         C_PV = pm.c_pv,  # [USD/kW] unit cost of PV
                         C_Wind = pm.c_wind, # [USD/kW] unit cost of W
                         C_BAT_energy = pm.c_bat_energy, # [USD/kWh] unit cost of battery energy storage
                         C_BAT_power = pm.c_bat_power,  # [USD/kW] unit cost of battery power capacpity
                         C_heater = pm.c_heater, # [USD/kW] unit cost of heater
                         PV_ref_capa = pv_ref_capa,    #capacity of reference PV plant (kW)
                         PV_ref_out = pv_ref_out,           #power output from reference PV plant (kW)
                         Wind_ref_capa = wind_ref_capa,      #capacity of reference wind farm (kW)
                         Wind_ref_out = wind_ref_out,        #power output from the reference wind farm (kW)
                         L = [P_load_des for i in range(len(pv_ref_out))],  #[kW] load profile timeseries
                         r_pv= r_pv)  # pv ratio


    elif model_name=='pv_battery_heat':
        P_heater=P_load_des/pm.eta_heater
        simparams = dict(DT = 1.,# [h] time steps
                         RM = RM, # renewable multiple
                         t_storage = t_storage, # [h] storage hour
                         BAT_ETA_in = pm.eta_bat_in,   # charging efficiency of battery
                         BAT_ETA_out = pm.eta_bat_out,  # discharg efficiency of battery
                         P_heater = P_heater, # [kW] heater designed power
                         ETA_heater = pm.eta_heater, # heater efficiency
                         C_PV = pm.c_pv,  # [USD/kW] unit cost of PV
                         C_BAT_energy = pm.c_bat_energy, # [USD/kWh] unit cost of battery energy storage
                         C_BAT_power = pm.c_bat_power,  # [USD/kW] unit cost of battery power capacpity
                         C_heater = pm.c_heater, # [USD/kW] unit cost of heater
                         PV_ref_capa = pv_ref_capa,    #capacity of reference PV plant (kW)
                         PV_ref_out = pv_ref_out,           #power output from reference PV plant (kW)
                         L = [P_load_des for i in range(len(pv_ref_out))])  #[kW] load profile timeseries



    elif model_name=='pv_wind_TES_heat':
        P_heater=P_load_des/pm.eta_heater
        simparams = dict(DT = 1.,# [h] time steps
                         RM = RM, # renewable multiple
                         t_storage = t_storage, # [h] storage hour
                         eta_TES_in = pm.eta_TES_in,   # charging efficiency of battery
                         eta_TES_out = pm.eta_TES_out,  # discharg efficiency of battery
                         P_heater = P_heater, # [kW] heater designed power
                         eta_heater = pm.eta_heater, # heater efficiency
                         c_PV = pm.c_pv,  # [USD/kW] unit cost of PV
                         c_Wind = pm.c_wind, # [USD/kW] unit cost of W
                         c_TES = pm.c_TES, # [USD/kWh] unit cost of TES
                         c_heater = pm.c_heater, # [USD/kW] unit cost of heater
                         PV_ref_capa = pv_ref_capa,    # capacity of reference PV plant (kW)
                         PV_ref_out = pv_ref_out,           #power output from reference PV plant (kW)
                         Wind_ref_capa = wind_ref_capa,      #capacity of reference wind farm (kW)
                         Wind_ref_out = wind_ref_out,        #power output from the reference wind farm (kW)
                         L = [P_load_des for i in range(len(pv_ref_out))],  #[kW] load profile timeseries
                         r_pv= r_pv)  # pv ratio



    #run the optimisation function and get the results in a dictionary:
    genDZN=GenDZN(model_name, simparams, casedir)
    dzn_fn=genDZN.dzn_fn
    results = optimise(model_name, dzn_fn, casedir)

    output=Outputs(verbose)
    if 'pv_wind_battery_heat' in model_name:
        output.pv_wind_battery_heat_outputs(results, casedir)

    elif model_name=='pv_battery_heat':
        output.pv_battery_heat_outputs(results, casedir)

    elif model_name=='wind_battery_heat':
        output.wind_battery_heat_outputs(results, casedir)

    elif model_name=='pv_wind_TES_heat':
        output.pv_wind_TES_heat_outputs(results, casedir)




if __name__=='__main__':
    location='Newman'
    SH=np.arange(0, 20, 2)
    RM=np.append(np.arange(1, 5, 0.5), np.arange(5, 11, 2))
    model_name='pv_wind_battery_heat'

    for rm in RM:
        for sh in SH:
            casedir='./results/%s/%s-wind-only/'%(model_name, location)
            res_fn=casedir+'/summary_%.1f_%.1f.csv'%(rm, sh)
            if not os.path.exists(res_fn):

                try:
                    master(model_name, location, rm, sh, P_load_des=500e3, r_pv=0, casedir=casedir, verbose=False)
                    print('RM', rm, 'SH', sh, 'Done')
                except:
                    print('RM', rm, 'SH', sh, 'Unsolved')

            else:
                print('RM', rm, 'SH', sh, 'Done')



