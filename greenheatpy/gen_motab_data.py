"""
Created on Tue Jan 10 10:52:26 2023 @author: Ye Wang
For generating the input data (the reference pv/wind power output) for the Openmodelica system models

"""

import numpy as np
import matplotlib.pyplot as plt
import os
from greenheatpy.pySAM_models import pv_gen, wind_gen, cst_gen
from greenheatpy.get_weather_data import SolarResource, WindSource

def gen_ref_power(model_name, location, casedir, plot=False, solcast_TMY=False):
    '''
    Arguments:
        model_name (str): pv or wind
        location (str): location name
        casedir (str): directory to save the data
        solcast_TMY (bool): True to use solcast_TMY data, False to use the data in data/weather folder (from Windlab)

    Return:
        A motab data file that is saved in the case directory
    '''

    if model_name=='pv':
        solar_data_fn=SolarResource(location, casedir=casedir, solcast_TMY=solcast_TMY) 
        pv_ref_capa = 1e3 #(kW)
        output_fn = pv_gen(pv_ref_capa, location=location, casedir=casedir, wea_fn=solar_data_fn)   
        name='PV_out_ref'
   
    elif model_name=='wind':
        wind_data_fn=WindSource(location, casedir=casedir, solcast_TMY=solcast_TMY)        
        wind_ref_capa = 320e3 #(kW)
        output_fn = wind_gen(wind_ref_capa, location=location, casedir=casedir, wea_fn=wind_data_fn)    
        name='Wind_out_ref'

    with open(output_fn) as f:
        output=f.readlines()
    f.close()  

    data=output[0][1:-1].split(',')  
    data=np.array([float(x) for x in data])   
    if model_name=='pv':
        print('%s design capacity factor'%model_name, np.sum(data)/pv_ref_capa/365./24.)  
    elif model_name=='wind':
        print('%s design capacity factor'%model_name, np.sum(data)/wind_ref_capa/365./24.) 


    savefile=casedir+'/%s_%s.motab'%(name, location)
    f=open(savefile, 'w')
    f.write('#1\n') 
    f.write('#METALABELS, time, %s\n'%name)
    f.write('double %s(8760,2)\n'%name)  
    for i in range(8760):
        f.write('%s, %s\n'%(3600*i, data[i]))
    f.close()    

    if plot:
        plt.plot(np.arange(8760)/24., data)
        plt.xlabel('Time (day)')
        plt.ylabel('Power generation (kW)')
        plt.show()
        plt.close()
    return savefile

if __name__=='__main__':
    model_name='wind'
    location='Burnie 2'
    casedir='.'
    plot=True

    gen_ref_power(model_name, location, casedir, plot)


     
