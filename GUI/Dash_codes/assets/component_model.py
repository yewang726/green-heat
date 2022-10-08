# -*- coding: utf-8 -*-
"""
Created on Fri May  6 12:46:54 2022

@author: Ahmad Mojiri
"""
from projdirs import datadir

import numpy as np
import pandas as pd
import json, platform
import PySAM.Pvwattsv8 as PVWatts, Windpower

################################################################
def pv_gen(capacity):
    """
    Parameters
    ----------
    capacity in kW

    Returns system powr generated in W for each hour in a year
    
    """
    pv = PVWatts.new()
    
    
    dir = datadir + ['\SAM INPUTS\SOLAR\\', '/SAM INPUTS/SOLAR/'][platform.system()=='Linux']
    file_name = 'pvfarm_pvwattsv8'
    module = pv
    
    with open(dir + file_name + ".json", 'r') as file:
        data = json.load(file)
        for k,v in data.items():
            if k != "number_inputs":
                module.value(k, v)
    
    # module.SystemDesign.system_capacity = capacity
    pv.execute()
    output = np.array(pv.Outputs.gen)
    return(output.tolist())

#################################################################
def wind_gen(hub_height=150):
    """
    Parameters
    ----------
    Capacity will be added later

    Returns wind powr generated in W for each hour in a year
    
    """
    wind = Windpower.new()
    
    dir = datadir + ['\SAM INPUTS\WIND\\', '/SAM INPUTS/WIND/'][platform.system()=='Linux']
    file_name = 'windfarm_windpower'
    module = wind
    
    with open(dir + file_name + ".json", 'r') as file:
        data = json.load(file)
        for k,v in data.items():
            if k != "number_inputs":
                module.value(k, v)
    file.close()
    # module.SystemDesign.system_capacity = capacity
    wind.Turbine.wind_turbine_hub_ht = hub_height
    wind.execute()
    output = np.array(wind.Outputs.gen)
    return(output.tolist())

#################################################################
 #################################################################
def SolarResource(Location):
    """
    Parameters
    ----------
    None
        
    Returns
    -------
    copies the weather data into SOLAR folder for SAM.

    """
    WD_file = 'weather_data_%s.csv'%(Location)
    
    if platform.system()=='Linux':
        path = r'/home/ahmadmojiri/GreenH2/DATA/SAM_INPUTS/WEATHER_DATA/'
    else:
        path = r'C:\Nextcloud\HILT-CRC---Green-Hydrogen\DATA\SAM_INPUTS\WEATHER_DATA\\'
    data = pd.read_csv(path +"%s"%(WD_file))
    
    data_text = data.to_csv(index=False, line_terminator='\n')
    
    
    
    #write solare data
    if platform.system()=='Linux':
        path = r'/home/ahmadmojiri/GreenH2/DATA/SAM_INPUTS/SOLAR/'
    else:
        path = r'C:\Nextcloud\HILT-CRC---Green-Hydrogen\DATA\SAM_INPUTS\Solar\\'
    
       
    text_file = open(path + "SolarSource.csv", "w")
    text_file.write(data_text)
    text_file.close()
    print('Solar data file was generated from Solcast database!')

 #################################################################
def WindSource(Location):
    """
    Generates the wind source data for SAM based on the weather data 
    that is stored in WEATHER folder
    
    Returns
    -------
    None.
    
    """
    WD_file = 'weather_data_%s.csv'%(Location)
    
    if platform.system()=='Linux':
        path = r'/home/ahmadmojiri/GreenH2/DATA/SAM_INPUTS/WEATHER_DATA/'
    else:
        path = r'C:\Nextcloud\HILT-CRC---Green-Hydrogen\DATA\SAM_INPUTS\WEATHER_DATA\\'
    
    data = pd.read_csv(path + "%s"%(WD_file), skiprows=0)
    Lat = data.lat[0]
    Lon = data.lon[0]
    data = pd.read_csv(path + "%s"%(WD_file), skiprows=2)
    
    data_10 = data.iloc[:,[5,14,15,16]].copy()
    data_10.Pressure=data_10.Pressure/1013.25
    data_10 = data_10.rename(columns = {'Temperature':'T',
                                        'Wind Speed':'S',
                                        'Wind Direction':'D',
                                        'Pressure':'P'})
    heading_10 = pd.DataFrame({'T':['Temperature','C',10],
                               'S':["Speed", 'm/s',10],
                               'D':["Direction",'degrees',10],
                               'P':['Pressure','atm',10]})
    
    data_10 = heading_10.append(data_10).reset_index(drop=True)
    
    data = data_10.copy()
    Z_anem = 10
    
    Z = 40
    data_40 = data_10.copy()
    data_40.iloc[2,:]=Z
    data_temp = data_40.iloc[3:].copy()
    S = data_temp['S'].apply(lambda x:speed(40, 10, x) )
    data_temp.S = S
    data_40 = data_40.iloc[0:3].append(data_temp,ignore_index=True)
    data = pd.concat([data , data_40],axis=1)
    
    Z = 70
    data_70 = data_10.copy()
    data_70.iloc[2,:]=Z
    data_temp = data_70.iloc[3:].copy()
    S = data_temp['S'].apply(lambda x:speed(70, 10, x) )
    data_temp.S = S
    data_70 = data_70.iloc[0:3].append(data_temp,ignore_index=True)
    data = pd.concat([data , data_70],axis=1)
    
    Z = 100
    data_100 = data_10.copy()
    data_100.iloc[2,:]=Z
    data_temp = data_100.iloc[3:].copy()
    S = data_temp['S'].apply(lambda x:speed(100, 10, x) )
    data_temp.S = S
    data_100 = data_100.iloc[0:3].append(data_temp,ignore_index=True)
    data = pd.concat([data , data_100],axis=1)
    
    Z = 130
    data_130 = data_10.copy()
    data_130.iloc[2,:]=Z
    data_temp = data_130.iloc[3:].copy()
    S = data_temp['S'].apply(lambda x:speed(130, 10, x) )
    data_temp.S = S
    data_130 = data_130.iloc[0:3].append(data_temp,ignore_index=True)
    data = pd.concat([data , data_130],axis=1)
    
    Z = 160
    data_160 = data_10.copy()
    data_160.iloc[2,:]=Z
    data_temp = data_160.iloc[3:].copy()
    S = data_temp['S'].apply(lambda x:speed(160, 10, x) )
    data_temp.S = S
    data_160 = data_160.iloc[0:3].append(data_temp,ignore_index=True)
    data = pd.concat([data , data_160],axis=1)
    
    
    data.loc[-1] = 24*['Latitude:%s'%(Lat)]
    data.index = data.index+1
    data.sort_index(inplace=True)
    data.loc[-1] = 24*['Longitude:%s'%(Lon)]
    data.index = data.index+1
    data.sort_index(inplace=True)
    
    data_text = data.to_csv(header=False, index=False, line_terminator='\n')
    
    #write wind data
    if platform.system()=='Linux':
        path = r'/home/ahmadmojiri/GreenH2/DATA/SAM_INPUTS/WIND/'
    else:
        path = r'C:\Nextcloud\HILT-CRC---Green-Hydrogen\DATA\SAM_INPUTS\WIND\\'
    
    
    text_file = open(path + "WindSource.csv", "w")
    text_file.write(data_text)
    text_file.close()
    print("Wind source data file was generated from Solcast database!")
   
 #################################################################
def speed(Z,Z_anem,U_anem):
    """
    This function calculates the logarithmic wind speed as a function of 
    heigth
    
    Parameters
    ----------
    Z: height of interest
    Z_anem: anemometer heigth
    U_anem: wind speed at anemometer height

    Returns wind speed at Z
        
    """
    Z0 = 0.01
    U_H = U_anem * np.log(Z/Z0)/np.log(Z_anem/Z0)
    return(U_H)

    