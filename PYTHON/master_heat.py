import pandas as pd
import numpy as np
import os
from projdirs import datadir #load the path that contains the data files 
from PACKAGE.optimisation_green_heat import optimise
from PACKAGE.component_model import WindSource, SolarResource,pv_gen, wind_gen, cst_gen, solcast_weather, SolarResource_solcast, WindSource_solcast
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

    #TODO the weather data is loaded from the pre-saved data in data dir
    # it is Newman TMY from Solcast, sent by AM on 24 Jun
    # this part will be updated when the Solcast access is solved
    if 'pv' in model_name:
        # Get solar data
        #if not os.path.exists(casedir+'/SolarSource.epw'):
        #    SolarResource(Lat,Lon, casedir)
        # Get SAM reference system outputs
        pv_ref_capa = 1e3 #(kW)
        pv_ref_out = pv_gen(pv_ref_capa, wea_dir=None)        


    if 'wind' in model_name:
        # Get wind data
        #if not os.path.exists(casedir+'/WindSource.csv'):
        #    WindSource(Lat, Lon, casedir)
        # Get SAM reference system outputs
        wind_ref_capa = 200e3 #(kW)
        wind_ref_out = wind_gen(wind_ref_capa, wea_dir=None)


    if 'CST' in model_name:
        #if not os.path.exists(casedir+'/SolarSource.epw'):
        #    SolarResource(Lat,Lon, casedir)
        # Get SAM output 
        P_recv_out, H_recv, D_recv, H_tower, n_helios, A_land = cst_gen(Q_des_th=P_load_des, SM=RM, wea_dir=None)

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


    elif model_name=='CST_TES_heat':
        simparams = dict(DT = 1.,# [h] time steps
                         t_storage = t_storage, # [h] storage hour
                         eta_TES_in = pm.eta_TES_in,   # charging efficiency of battery
                         eta_TES_out = pm.eta_TES_out,  # discharg efficiency of battery
                         P_recv_out = P_recv_out,        #power output from the reference wind farm (kW)
                         L = [P_load_des for i in range(len(P_recv_out))])  #[kW] load profile timeseries


    #run the optimisation function and get the results in a dictionary:
    casename=model_name+'_%.2f_%.2f'%(RM, t_storage)
    genDZN=GenDZN(model_name, simparams, casename, casedir)
    dzn_fn=genDZN.dzn_fn
    results = optimise(model_name, dzn_fn, casedir)

    output=Outputs(verbose)

    CF=results['CF'][0]
    if 'pv_wind_battery_heat' in model_name:

        CAPEX=results['CAPEX'][0]
        pv_max = results['pv_max'][0]
        wind_max = results['wind_max'][0]
        OM_fixed=pm.c_om_fixed_pv*pv_max+pm.c_om_fixed_wind*wind_max
        c_OM_var = 0.
        C_direct= CAPEX*(1.+pm.r_conting)
        C_indirect = (pm.r_EPC+pm.r_tax)*C_direct #TODO and C_land
        C_cap=C_direct + C_indirect
        LCOH=cal_LCOH(CF,  P_load_des, C_cap, OM_fixed, c_OM_var, r_discount=pm.r_disc_real, t_life=pm.t_life, t_cons=pm.t_cons)
        output.pv_wind_battery_heat_outputs(results, casedir, LCOH)

    elif model_name=='pv_battery_heat':


        CAPEX=results['CAPEX'][0]
        pv_max = results['pv_max'][0]
        OM_fixed=pm.c_om_fixed_pv*pv_max
        c_OM_var = 0.
        C_direct= CAPEX*(1.+pm.r_conting)
        C_indirect = (pm.r_EPC+pm.r_tax)*C_direct #TODO and C_land
        C_cap=C_direct + C_indirect
        LCOH=cal_LCOH(CF,  P_load_des, C_cap, OM_fixed, c_OM_var, r_discount=pm.r_disc_real, t_life=pm.t_life, t_cons=pm.t_cons)

        output.pv_battery_heat_outputs(results, casedir, LCOH)

    elif model_name=='pv_wind_TES_heat':

        CAPEX=results['CAPEX'][0]
        pv_max = results['pv_max'][0]
        wind_max = results['wind_max'][0]
        OM_fixed=pm.c_om_fixed_pv*pv_max+pm.c_om_fixed_wind*wind_max
        c_OM_var = 0.
        C_direct = CAPEX*(1.+pm.r_conting)
        C_indirect = (pm.r_EPC+pm.r_tax)*C_direct #TODO and C_land
        C_cap = C_direct + C_indirect
        LCOH = cal_LCOH(CF, P_load_des, C_cap, OM_fixed, c_OM_var, r_discount=pm.r_disc_real, t_life=pm.t_life, t_cons=pm.t_cons)
        output.pv_wind_TES_heat_outputs(results, casedir, LCOH)


    elif model_name=='CST_TES_heat':

        C_recv = pm.C_recv_ref * ( H_recv * D_recv * np.pi / pm.A_recv_ref)**pm.f_recv_scale
        C_tower = pm.C_tower_fixed * np.exp(pm.f_tower_scale * (H_tower - H_recv/2.+pm.H_helio/2.))
        C_field = pm.c_helio * n_helios * pm.A_helio
        C_site = pm.c_site_cst * pm.A_helio * n_helios
        C_TES = pm.c_TES * results['TES_capa'][0]
        C_land = pm.c_land * A_land
        CAPEX = C_recv + C_tower + C_field + C_site + C_TES
        OM_fixed=pm.c_om_fixed_cst * P_load_des
        c_OM_var = pm.c_om_var_cst
        C_direct= CAPEX*(1.+pm.r_conting)
        C_indirect = (pm.r_EPC+pm.r_tax)*C_direct + C_land 
        C_cap=C_direct + C_indirect
        LCOH=cal_LCOH(CF,  P_load_des, C_cap, OM_fixed, c_OM_var, r_discount=pm.r_disc_real, t_life=pm.t_life, t_cons=pm.t_cons)
        output.CST_TES_heat_outputs(results, casedir, RM, H_recv, D_recv, H_tower, n_helios, A_land, LCOH)
        #print('C_CAP', C_cap)
        #print('CF', CF)
        #print(RM, t_storage, H_recv, D_recv, H_tower, n_helios, A_land)
        #print('recv, %.0f, tower, %.0f,field, %.0f,site, %.0f,tes, %.0f,land, %.0f'%(C_recv, C_tower, C_field, C_site, C_TES, C_land) )


    print('LCOH', LCOH)
    print('CF', CF)
    print('C_cap', C_cap)
    if not verbose:
        os.system('rm '+ genDZN.dzn_fn)

    return LCOH, CF

def cal_LCOH(CF, load, C_cap, OM_fixed, c_OM_var, r_discount, t_life, t_cons):
    """Levelised cost of heat in USD/MWh. 
    Similar approach in SolarTherm for LCOE calculation.

    We take the convention that payments made or energy produced during a year
    are discounted at the end of that year. For example, the O&M
    costs M paid during the first year has a present value of M/(1 + r).  This
    will tend to underestimate costs but also underestimate the value of the
    energy produced. These will tend to cancel out, but there will remain a 
    difference between LCOE calculated using the start of the year.

    The capital costs are discounted at the start of the year instead, and are
    split over each year of construction. This should probably be handled with
    loans.
    Note that here the real discounted rate (i.e. r_discount) has been used to calculate
    the real LCOE.

    CF         (float): capacity factor
    load       (float): the design heat load of the system (kW)
    C_cap      (float): total capital cost (USD)
    OM_fixed   (float): cost of fixed O&M (USD/kW)
    c_OM_var   (float): unit cost of variable O&M (USD/kWh)
    r_discount (float): discount rate
    t_life     (int)  : lifetime of the system (y)   
    t_cons     (int)  : construction time (y)
    """
    nu = 0.
    de = 0.

    epy=CF*load*24.*365./1000. #MWh
    c_year=OM_fixed+c_OM_var*epy

    # Assume capital cost is evenly split between years in construction phase,
    # else if no construction phase it is all paid up front
    if t_cons == 0:
        nu += C_cap
    else:
        for i in range(t_cons):
            nu += (C_cap/t_cons)/((1 + r_discount)**i)

    for i in range(t_cons+1, t_cons+t_life+1):
        nu += c_year/((1 + r_discount)**i)
        de += epy/((1 + r_discount)**i)

    LCOH=nu/de

    return LCOH

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



