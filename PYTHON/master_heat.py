import pandas as pd
import numpy as np
import os
from projdirs import datadir #load the path that contains the data files 
from PACKAGE.optimisation_green_heat import make_dzn_file, optimise
from PACKAGE.component_model import WindSource, SolarResource,pv_gen, wind_gen,solcast_weather, SolarResource_solcast, WindSource_solcast

import matplotlib.pyplot as plt
# Set the location
'''
#Newman
Newman = [-23.35, 119.75]
Sydney = [-33.856784, 151.215297]
Tom_Price = [-22.69, 117.79]
Port_Augusta = [-32.49, 137.77]
Whyalla = [-33.04, 137.59]
Pinjarra = [-32.63, 115.87]
Gladstone = [-23.84, 151.25]
Burnie = [-41.05, 145.91]

# Get wind and solar data for the designated location
Lat=Newman[0]
Lon=Newman[1]
WindSource(Lat, Lon)
SolarResource(Lat,Lon)
'''

#solcast_weather(Newman)
#SolarResource_solcast()
#WindSource_solcast()

'''
### Set the inputs for plant optimisation and run the optimisation
pv_ref_capa = 1e6 #(W)
pv_ref_out = pv_gen(pv_ref_capa)

wind_ref_capa = 200e6 #(W)
wind_ref_out = wind_gen(wind_ref_capa)

def AUD2USD(value):
    return(0.746 * value)

# create a dictionary that contains the inputs for optimisation.
#these inputs are used by make_dzn_file function to create an input text file called hydrogen_plant_data.dzn. 
simparams = dict(DT = 3600,# [s] time steps
                 RM = 2, # renewable multiple
                 t_storage = 8, # [h] storage hour
                 BAT_ETA_in = 0.95,   # charging efficiency of battery
                 BAT_ETA_out = 0.95,  # discharg efficiency of battery
                 P_heater =500e6, # [W] heater designed power
                 ETA_heater = 0.99, # heater efficiency
                 C_PV = AUD2USD(1.258),  # [$/W] unit cost of PV
                 C_Wind = AUD2USD(1.934), # [$/W] unit cost of W
                 C_BAT_energy = AUD2USD(400/1000/3600), # [$/W.s] unit cost of battery energy storage
                 C_BAT_power = 60/1000,  # [$/W] unit cost of battery power capacpity
                 C_heater = 206/1000, # [$/W] unit cost of heater
                 PV_ref_capa = pv_ref_capa,    #capacity of reference PV plant (W)
                 PV_ref_out = pv_ref_out,           #power output from reference PV plant (W)
                 Wind_ref_capa = wind_ref_capa,      #capacity of reference wind farm (W)
                 Wind_ref_out = wind_ref_out,        #power output from the reference wind farm (W)
                 L = [500e6 for i in range(len(pv_ref_out))])       #[W] load profile timeseries

#run the optimisation function and get the results in a dictionary:
results = optimise(simparams)


CAPEX=results["CAPEX"][0]/1e6 # M.USD
CF=results["CF"][0]
RM=results["RM"][0]
t_storage=results["t_storage"][0]
r_pv=results["r_pv"][0]
pv_max=results["pv_max"][0]/1.e6 # MW
wind_max=results["wind_max"][0]/1.e6 # MW
bat_capa=results["bat_capa"][0]/1.e6/3600. # MWh
bat_pmax=results["bat_pmax"][0]/1.e6 # MW
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

np.savetxt('summary.csv', summary, fmt='%s', delimiter=',')
np.savetxt('pv_out.csv', pv_out, fmt='%.4f', delimiter=',')
np.savetxt('wind_out.csv', wind_out, fmt='%.4f', delimiter=',')
np.savetxt('P_curt.csv', P_curt, fmt='%.4f', delimiter=',')
np.savetxt('P_st_in.csv', P_st_in, fmt='%.4f', delimiter=',')
np.savetxt('P_st_out.csv', P_st_out, fmt='%.4f', delimiter=',')
np.savetxt('P_ele.csv', P_ele, fmt='%.4f', delimiter=',')
np.savetxt('P_heat.csv', P_heat, fmt='%.4f', delimiter=',')
np.savetxt('bat_e_stored.csv', bat_e_stored, fmt='%.4f', delimiter=',')
np.savetxt('load.csv', load, fmt='%.4f', delimiter=',')
'''

pv_out=np.loadtxt('pv_out.csv', delimiter=',')
wind_out=np.loadtxt('wind_out.csv',delimiter=',')
P_ele=np.loadtxt('P_ele.csv',delimiter=',')
P_curt=np.loadtxt('P_curt.csv', delimiter=',')
P_st_in=np.loadtxt('P_st_in.csv', delimiter=',')

print(np.max(P_curt))
time=np.arange(len(pv_out))
plt.plot(time, pv_out)
plt.plot(time, wind_out)
plt.plot(time, P_ele)
plt.plot(time, P_curt)
plt.plot(time, P_st_in)
plt.show()
plt.close()

print(np.max(pv_out+ wind_out - P_curt - pv_wind_direct - P_st_in))


# check
#pv_wind_direct=P_ele-P_st_out
#check=(pv_out+ wind_out - P_curt - pv_wind_direct - P_st_in != 0)
#print(np.sum(check))






