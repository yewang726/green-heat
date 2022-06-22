# -*- coding: utf-8 -*-
"""
Created on Fri May  6 12:46:54 2022

@author: Ahmad Mojiri
"""
from projdirs import datadir

import numpy as np
import pandas as pd
import json, io, requests
import PySAM.Pvwattsv8 as PVWatts, Windpower

import platform

################################################################
def pv_gen(capacity, wea_dir=None):
    """
    Parameters
    ----------
    capacity in kW

    Returns system powr generated in W for each hour in a year
    
    """
    module = PVWatts.new()

    if platform.system()=='Windows':
        json_fn=datadir+'\json_pvWatts\default_pvwattsv8.json' 
    elif platform.system()=='Linux':
        json_fn=datadir+'/json_pvWatts/default_pvwattsv8.json'   
  
    with open(json_fn, 'r') as f:
        data = json.load(f)
        for k,v in data.items():
            if k != "number_inputs":
                module.value(k, v)

    if wea_dir==None:
        module.value('solar_resource_file', datadir+'/SolarSource.epw')
    else:
        module.value('solar_resource_file', wea_dir+'/SolarSource.epw')

        
    module.SystemDesign.system_capacity = capacity
    module.execute()
    output = np.array(module.Outputs.gen)
    return(output.tolist())

#################################################################
def wind_gen(capacity, wea_dir=None):
    """
    Parameters
    ----------
    capacity in kW

    Returns wind powr generated in kW for each hour in a year
    
    """
    module = Windpower.new()

    if platform.system()=='Windows':
        json_fn=datadir+'\json_windpower\default_windpower.json' 
    elif platform.system()=='Linux':
        json_fn=datadir+'/json_windpower/default_windpower.json'   
    
    with open(json_fn, 'r') as f:
        data = json.load(f)
        for k,v in data.items():
            if k != "number_inputs":
                module.value(k, v)

    if wea_dir==None:
        module.value('wind_resource_filename', datadir+'/WindSource.csv')
    else:
        module.value('wind_resource_filename', wea_dir+'/WindSource.csv')

    module.value('system_capacity', capacity)
    
    module.execute()
    output = np.array(module.Outputs.gen)
    
    return(output.tolist())

#################################################################
def WindSource(Lat,Lon, casedir=None):
    """
    The function gets the TMY data from PVGIS:
        API = https://re.jrc.ec.europa.eu/api/v5_2/tmy
    
    Parameters
    ----------
    lat: Latitude
    long: longitude

    Returns a csv file in .srw format for wind farm modelling in SAM
        
    """
    url = 'https://re.jrc.ec.europa.eu/api/v5_2/tmy'

    Params = {'lat':Lat,
              'lon':Lon}
    
    response = requests.get(url,params=Params)
    print('Connection Status:', response.status_code)
    response.close()
    text = response.text
    
    text2 = 'time(UTC)'+ text.split('\ntime(UTC)')[1]
    text3 = text2.replace('\r\n\r\n','').split('T2m:')[0]
    
    if platform.system()=='Windows':
        text_file = open(datadir + "\weather_data.csv", "w")
    elif platform.system()=='Linux':
        text_file = open(datadir + "/weather_data.csv", "w")

    text_file.write(text3.replace('\r',''))
    text_file.close()
    print('Weather data file was downloaded!')
    
    data = io.StringIO(text3)
    data = pd.read_csv(data)
    data_10 = data.iloc[:,[1,7,8,9]].copy()
    data_10.SP=data_10.SP/101325
    data_10 = data_10.rename(columns = {'T2m':'T', 'WS10m':'S', 'WD10m':'D', 'SP':'P'})
    heading_10 = pd.DataFrame({'T':['Temperature','C',10], 'S':["Speed", 'm/s',10],
                               'D':["Direction",'degrees',10], 'P':['Pressure','atm',10]})
    data_10 = heading_10.append(data_10).reset_index(drop=True)
    data = data_10.copy()
    Z_anem = 10
    
    Z = 40
    data_40 = data_10.copy()
    data_40.iloc[2,:]=Z
    data_temp = data_40.iloc[3:].copy()
    S = data_temp.apply(lambda x:speed(Z, Z_anem, data_temp['S']) )

    data_temp.S = S.S
    data_40 = data_40.iloc[0:3].append(data_temp,ignore_index=True)
    data = pd.concat([data , data_40],axis=1)
    
    Z = 70
    data_70 = data_10.copy()
    data_70.iloc[2,:]=Z
    data_temp = data_70.iloc[3:].copy()
    S = data_temp.apply(lambda x:speed(Z, Z_anem, data_temp['S']) )
    data_temp.S = S.S
    data_70 = data_70.iloc[0:3].append(data_temp,ignore_index=True)
    data = pd.concat([data , data_70],axis=1)
    
    Z = 100
    data_100 = data_10.copy()
    data_100.iloc[2,:]=Z
    data_temp = data_100.iloc[3:].copy()
    S = data_temp.apply(lambda x:speed(Z, Z_anem, data_temp['S']) )
    data_temp.S = S.S
    data_100 = data_100.iloc[0:3].append(data_temp,ignore_index=True)
    data = pd.concat([data , data_100],axis=1)
    
    data.loc[-1] = 16*['Latitude:%d'%(Lat)]
    data.index = data.index+1
    data.sort_index(inplace=True)
    data.loc[-1] = 16*['Longitude:%d'%(Lon)]
    data.index = data.index+1
    data.sort_index(inplace=True)
    
    data_text = data.to_csv(header=False, index=False, line_terminator='\n')
    # data_text = 'Latitude:%d'%(Lat)+'\n' + 'Longitude:%d'%(Lon)+'\n' + data_text

    if platform.system()=='Windows':
        if casedir==None:
            text_file = open(datadir + "\WindSource.csv", "w")
        else:
            text_file = open(casedir + "\WindSource.csv", "w")            
    elif platform.system()=='Linux':
        if casedir==None:
            text_file = open(datadir + "/WindSource.csv", "w")
        else:
            text_file = open(casedir + "/WindSource.csv", "w")            

    text_file.write(data_text)
    text_file.close()
    print('Wind source file was created!')
    return('Wind source is ready!')
    
##################################################################
def SolarResource(Lat,Lon, casedir=None):
    """
    The function gets the TMY data from PVGIS:
        API = https://re.jrc.ec.europa.eu/api/v5_2/tmy
    
    Parameters
    ----------
    lat: Latitude
    long: longitude

    Returns a epw file in .epw format for PV modelling in SAM
        
    """
    url = 'https://re.jrc.ec.europa.eu/api/v5_2/tmy'

    Params = {'lat':Lat,
              'lon':Lon,
              'outputformat':'epw'}
    
    response = requests.get(url,params=Params)
    print('Connection Status:', response.status_code)
    response.close()
    
    data_text = response.text.replace('\r','')

    if platform.system()=='Windows':
        if casedir==None:
            text_file = open(datadir + "\SolarSource.epw", "w")
        else:
            text_file = open(casedir + "\SolarSource.epw", "w")
    elif platform.system()=='Linux':
        if casedir==None:
            text_file = open(datadir + "/SolarSource.epw", "w")
        else:
            text_file = open(casedir + "/SolarSource.epw", "w")

    text_file.write(data_text)
    text_file.close()
    print('Solar source file was created!')
    return('Solar source is ready!') 
    
##################################################################
def solcast_weather(location):
    """
    The function download tmy weather data from Solcast under a research
    account.

    Parameters
    ----------
    location : List object
         includes [latitude,longitude] of the location

    Returns a savd csv file in the format that can be used with SAM for PV
    modelling.
    """
    base_url = 'https://api.solcast.com.au/'
    tool = 'tmy_hourly?api_key='
    key = 'YNEmGUM8_CfnWlNPinB9d3EnlGVpFwWV'
    Parameters = {}
    Parameters = dict(zip(['api_key','format','latitude','longitude'],
                          [key,'x-sam+csv']+ location,
                          ))
    
    url = 'https://api.solcast.com.au/'
    values = {'username': 'joe.coventry@anu.edu.au',
          'password': 'hiltcrc'}
    r = requests.post(url, data=values)
    
    response = requests.get(base_url+tool,params=Parameters)
    print('Connection Status:', response.status_code)
    response.close()
    
    if platform.system()=='Windows':
        text_file = open(datadir + "\weather_data_solcast.csv", "w")
    elif platform.system()=='Linux':
        text_file = open(datadir + "/weather_data_solcast.csv", "w")

    text_file.write(response.text)
    text_file.close()
    print('Weather data was downloaded from Solcast database!')

 #################################################################
def SolarResource_solcast():
    """
    Parameters
    ----------
    None
        
    Returns
    -------
    copies the weather data into SOLAR folder for SAM.

    """

    if platform.system()=='Windows':
        data = data = pd.read_csv(datadir + "\weather_data_solcast.csv")
    elif platform.system()=='Linux':
        data =pd.read_csv(datadir + "/weather_data_solcast.csv")
    
    data_text = data.to_csv(index=False, line_terminator='\n')

    if platform.system()=='Windows':
        text_file = open(datadir + "\SolarSource.csv", "w")
    elif platform.system()=='Linux':
        text_file = open(datadir + "/SolarSource.csv", "w")

    text_file.write(data_text)
    text_file.close()
    print('Solar data file was generated from Solcast database!')

 #################################################################
def WindSource_solcast():
    """
    Generates the wind source data for SAM based on the weather data 
    that is stored in WEATHER folder
    
    Returns
    -------
    None.
    
    """

    if platform.system()=='Windows':
        data = pd.read_csv(datadir + "\weather_data_solcast.csv", skiprows=0)
        Lat = data.lat[0]
        Lon = data.lon[0]
        data = pd.read_csv(datadir + "\weather_data_solcast.csv", skiprows=2)
    elif platform.system()=='Linux':
        data = pd.read_csv(datadir + "/weather_data_solcast.csv", skiprows=0)
        Lat = data.lat[0]
        Lon = data.lon[0]
        data = pd.read_csv(datadir + "/weather_data_solcast.csv", skiprows=2)

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
    S = data_temp.apply(lambda x:speed(Z, Z_anem, data_temp['S']) )
    data_temp.S = S
    data_40 = data_40.iloc[0:3].append(data_temp,ignore_index=True)
    data = pd.concat([data , data_40],axis=1)
    
    Z = 70
    data_70 = data_10.copy()
    data_70.iloc[2,:]=Z
    data_temp = data_70.iloc[3:].copy()
    S = data_temp.apply(lambda x:speed(Z, Z_anem, data_temp['S']) )
    data_temp.S = S
    data_70 = data_70.iloc[0:3].append(data_temp,ignore_index=True)
    data = pd.concat([data , data_70],axis=1)
    
    Z = 100
    data_100 = data_10.copy()
    data_100.iloc[2,:]=Z
    data_temp = data_100.iloc[3:].copy()
    S = data_temp.apply(lambda x:speed(Z, Z_anem, data_temp['S']) )
    data_temp.S = S
    data_100 = data_100.iloc[0:3].append(data_temp,ignore_index=True)
    data = pd.concat([data , data_100],axis=1)
    
    data.loc[-1] = 16*['Latitude:%s'%(Lat)]
    data.index = data.index+1
    data.sort_index(inplace=True)
    data.loc[-1] = 16*['Longitude:%s'%(Lon)]
    data.index = data.index+1
    data.sort_index(inplace=True)
    
    data_text = data.to_csv(header=False, index=False, line_terminator='\n')

    if platform.system()=='Windows':
        text_file = open(datadir + "\WindSource.csv", "w")
    elif platform.system()=='Linux':
        text_file = open(datadir + "/WindSource.csv.csv", "w")

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
    Z0 = 0.003
    U_H = U_anem * np.log(Z/Z0)/np.log(Z_anem/Z0)
    return(U_H)   
