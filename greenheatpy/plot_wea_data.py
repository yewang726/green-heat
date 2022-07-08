import matplotlib.pyplot as plt
import pandas as pd
from projdirs import datadir

def plot_compare(wea_fn1, wea_fn2, name1, name2):

    df1=pd.read_csv(wea_fn1)
    df2=pd.read_csv(wea_fn2)

    new_header=df1.iloc[1]
    data1=df1.iloc[2:].copy()
    data2=df2.iloc[2:].copy()
    data1.columns=new_header 
    data2.columns=new_header

    dataname=['DNI', 'DHI', 'GHI', 'Pressure', 'Wind Direction', 'Wind Speed', 'Temperature', 'Azimuth', 'Zenith', 'Cloud Opacity', 'Dew Point', 'Snow Depth']
    for dn in dataname:
    # DNI
        diff =data1[dn].astype(float)-data2[dn].astype(float)
        plt.plot(data1.index, diff, label=dn)


    plt.legend()
    plt.show()
    plt.close()

if __name__=='__main__':
    name1='Solcast online'
    name2='TMY repo'
    wea_fn1=datadir+'/SolarSource.csv'
    wea_fn2=datadir+'/SolarSource_Newman.csv'
    plot_compare(wea_fn1, wea_fn2, name1, name2)
    
          
