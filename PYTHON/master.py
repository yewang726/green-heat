import pandas as pd
import numpy as np
import os
from projdirs import datadir #load the path that contains the data files 
from PACKAGE.optimisation import make_dzn_file, optimise
from PACKAGE.component_model import WindSource, SolarResource,pv_gen, wind_gen,solcast_weather, SolarResource_solcast, WindSource_solcast

# Set the location

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


#solcast_weather(Newman)
#SolarResource_solcast()
#WindSource_solcast()


### Set the inputs for plant optimisation and run the optimisation
pv_ref_capa = 1e6 #(W)
pv_ref_out = pv_gen(pv_ref_capa)

wind_ref_capa = 50e6 #(W)
wind_ref_out = wind_gen()

def AUD2USD(value):
    return(0.746 * value)

# create a dictionary that contains the inputs for optimisation.
#these inputs are used by make_dzn_file function to create an input text file called hydrogen_plant_data.dzn. 
simparams = dict(DT = 3600,#[s] time steps
                 ETA_EL = 0.70,       #efficiency of electrolyser
                 BAT_ETA_in = 0.95,   #charging efficiency of battery
                 BAT_ETA_out = 0.95,  #discharg efficiency of battery
                 C_PV = AUD2USD(1.258),          #[$/W] unit cost of PV
                 C_W = AUD2USD(1.934),           #[$/W] unit cost of W
                 C_EL = 0.835,          #[$/W] unit cost of electrolyser
                 C_HS = 95,           #[$/kgH] unit cost of hydrogen storage
                 C_BAT_energy = AUD2USD(400/1000/3600),        #[$/W.s] unit cost of battery energy storage
                 C_BAT_power = 60/1000,        #[$/W] unit cost of battery power capacpity
                 CF = 0.95,           #capacity factor
                 PV_ref_capa = pv_ref_capa,    #capacity of reference PV plant (W)
                 PV_ref_out = pv_ref_out,           #power output from reference PV plant (W)
                 Wind_ref_capa = wind_ref_capa,      #capacity of reference wind farm (W)
                 Wind_ref_out = wind_ref_out,        #power output from the reference wind farm (W)
                 L = [0.1 for i in range(len(pv_ref_out))])       #[kgH2/s] load profile timeseries

#run the optimisation function and get the results in a dictionary:
results = optimise(simparams)

      
print ( '\nResults',
        '\nCAPEX = %0.2f [M$]' %( results['CAPEX'][0]/1e6 ),
        '\nPV rated capacity  = %0.2f [MW]' %( results['pv_max'][0]/1e6 ),  
        '\nWind rated capacity = %0.2f [MW]' %( results['w_max'][0]/1e6 ),    
        '\nElectrolyser rated capacity = %0.4f [MW]' %( results['el_max'][0]/1e6 ),  
        '\nHydrogen storage capacity = %0.2f [T of H2]' %( results['hs_max'][0]/1e3 ),  
        '\nBattery energy capacity = %0.2f [MWh]' %( results['bat_capa'][0]/3.6e9  ),  
        '\nBattery power capcity = %0.2f [MW]' %( results['bat_pmax'][0]/1e6 )
        )
