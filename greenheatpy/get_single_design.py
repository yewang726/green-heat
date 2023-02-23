'''
Get a specific design by interpolating the SH-RM data

'''

import numpy as np
from greenheatpy.parameters import Parameters, CST_SL_OM
from greenheatpy.master import cal_LCOH
from greenheatpy.projdirs import datadir
from greenheatpy.get_green_h2 import get_best_location

def get_CST_design(rm, sh, location, case, resdir, year=2020):


    CF_data=np.loadtxt('%s/post/2020/%s-%s-data_CF.csv'%(resdir, case, location), delimiter=',')
    Aland_data=np.loadtxt('%s/post/2020/%s-%s-data_Aland.csv'%(resdir, case, location), delimiter=',', skiprows=1)
    Drecv_data=np.loadtxt('%s/post/2020/%s-%s-data_Drecv.csv'%(resdir, case, location), delimiter=',', skiprows=1)
    Hrecv_data=np.loadtxt('%s/post/2020/%s-%s-data_Hrecv.csv'%(resdir, case, location), delimiter=',', skiprows=1)
    Htower_data=np.loadtxt('%s/post/2020/%s-%s-data_Htower.csv'%(resdir, case, location), delimiter=',', skiprows=1)
    Nhelio_data=np.loadtxt('%s/post/2020/%s-%s-data_Nhelio.csv'%(resdir, case, location), delimiter=',', skiprows=1)

    CF=CF_data[1:,1:]
    RM=CF_data[1:,0]
    SH=CF_data[0,1:]

    Aland=Aland_data[:,1]
    Drecv=Drecv_data[:,1]
    Hrecv=Hrecv_data[:,1]
    Htower=Htower_data[:,1]
    Nhelio=Nhelio_data[:,1]


    x=sh
    y=rm

    idx=np.argmin(abs(RM-rm))
    if RM[idx]!=1:
        row=idx-1
    else:
        row=idx

    idx=np.argmin(abs(SH-sh))
    if SH[idx]>0:
        col=idx-1
    else:
        col=idx

    x_1=SH[col]
    x_2=SH[col+1]
    y_1=RM[row]
    y_2=RM[row+1]
    Q_11=CF[row,col]
    Q_12=CF[row+1,col]
    Q_21=CF[row,col+1]
    Q_22=CF[row+1,col+1]
    CF=1/((x_2-x_1)*(y_2-y_1))*(Q_11*(x_2-x)*(y_2-y)+Q_21*(x-x_1)*(y_2-y)+Q_12*(x_2-x)*(y-y_1)+Q_22*(x-x_1)*(y-y_1))


    x1=RM[row]
    x2=RM[row+1]
    y1=Aland[row]
    y2=Aland[row+1]
    A_land=y2-(x2-rm)*(y2-y1)/(x2-x1)

    x1=RM[row]
    x2=RM[row+1]
    y1=Drecv[row]
    y2=Drecv[row+1]
    D_recv=y2-(x2-rm)*(y2-y1)/(x2-x1)

    x1=RM[row]
    x2=RM[row+1]
    y1=Hrecv[row]
    y2=Hrecv[row+1]
    H_recv=y2-(x2-rm)*(y2-y1)/(x2-x1)

    x1=RM[row]
    x2=RM[row+1]
    y1=Htower[row]
    y2=Htower[row+1]
    H_tower=y2-(x2-rm)*(y2-y1)/(x2-x1)

    x1=RM[row]
    x2=RM[row+1]
    y1=Nhelio[row]
    y2=Nhelio[row+1]
    n_helios=int(y2-(x2-rm)*(y2-y1)/(x2-x1))+1.

    P_load=500.e3
    TES_capa=P_load*sh

    return CF, A_land, D_recv, H_recv, H_tower, n_helios, TES_capa

 

def get_CST_modular_design(rm, sh, location, case, resdir, year=2020):

    CF_data=np.loadtxt('%s/post/2020/%s-%s-data_CF.csv'%(resdir, case, location), delimiter=',')
    num_modules=np.loadtxt('%s/post/2020/%s-%s-data_num_modules.csv'%(resdir, case, location), delimiter=',', skiprows=1)


    CF=CF_data[1:,1:]
    RM=CF_data[1:,0]
    SH=CF_data[0,1:]

    num_modules=num_modules[:,1]

    x=sh
    y=rm

    idx=np.argmin(abs(RM-rm))
    if RM[idx]!=1:
        row=idx-1
    else:
        row=idx

    idx=np.argmin(abs(SH-sh))
    if SH[idx]>0:
        col=idx-1
    else:
        col=idx

    x_1=SH[col]
    x_2=SH[col+1]
    y_1=RM[row]
    y_2=RM[row+1]
    Q_11=CF[row,col]
    Q_12=CF[row+1,col]
    Q_21=CF[row,col+1]
    Q_22=CF[row+1,col+1]
    CF=1/((x_2-x_1)*(y_2-y_1))*(Q_11*(x_2-x)*(y_2-y)+Q_21*(x-x_1)*(y_2-y)+Q_12*(x_2-x)*(y-y_1)+Q_22*(x-x_1)*(y-y_1))


    x1=RM[row]
    x2=RM[row+1]
    y1=num_modules[row]
    y2=num_modules[row+1]
    num_modules=y2-(x2-rm)*(y2-y1)/(x2-x1)


    module_power =1250 #MWrh
    #TODO this part made the simulation slow
    '''
    best=get_best_location(2020)
    loc=location+' %s'%best[location]
    output_fn=datadir+'modular_cst_design/CST_gen_%s_load%.1fMWth.dat'%(loc, module_power)
    with open(output_fn) as f:
        cst_output=f.read().splitlines()
    f.close()
    H_recv, D_recv, H_tower, n_helios, A_land = np.float_(cst_output[2].split(','))
    '''
    if location=='Burnie':
        H_recv=25.68
        D_recv=22.23
        H_tower=259.94
        n_helios=17361
        A_land= 19909374.49
    elif location=='Gladstone':
        H_recv=25.82
        D_recv=22.27
        H_tower=260.72
        n_helios=17094
        A_land=19509973.30   
    elif location=='Pilbara':
        H_recv=26.20
        D_recv=22.09
        H_tower=259.68
        n_helios=17314
        A_land=19833258.22   
    elif location=='Pinjara':
        H_recv=25.699
        D_recv=22.46
        H_tower=259.20
        n_helios=17261
        A_land=19797561.38  
    elif location=='Upper Spencer Gulf':
        H_recv=25.67
        D_recv=22.43
        H_tower=258.92
        n_helios=17159
        A_land= 19673291.19   


    P_load=500.e3
    TES_capa=P_load*sh

    return CF, A_land, D_recv, H_recv, H_tower, n_helios, TES_capa, num_modules


def get_TES_design(rm, sh, location, case,  resdir, year=2020, F_pv=None):
    '''
    year (int): year basis of the design
    costmodel (str): '2020', '2030', '2050', '2020_ub', ''2020_lb'
    '''

    CF_data=np.loadtxt('%s/post/%s/%s-%s-data_CF.csv'%(resdir, year, case, location), delimiter=',')
    Pheater_data=np.loadtxt('%s/post/%s/%s-%s-data_P_heater.csv'%(resdir, year, case, location), delimiter=',')


    CF=CF_data[1:,1:]
    P_heater=Pheater_data[1:,1:]
    RM=CF_data[1:,0]
    SH=CF_data[0,1:]


    x=sh
    y=rm

    idx=np.argmin(abs(RM-rm))
    if RM[idx]!=1:
        row=idx-1
    else:
        row=idx

    idx=np.argmin(abs(SH-sh))
    if SH[idx]>0:
        col=idx-1
    else:
        col=idx

    x_1=SH[col]
    x_2=SH[col+1]
    y_1=RM[row]
    y_2=RM[row+1]
    Q_11=CF[row,col]
    Q_12=CF[row+1,col]
    Q_21=CF[row,col+1]
    Q_22=CF[row+1,col+1]
    cf=1/((x_2-x_1)*(y_2-y_1))*(Q_11*(x_2-x)*(y_2-y)+Q_21*(x-x_1)*(y_2-y)+Q_12*(x_2-x)*(y-y_1)+Q_22*(x-x_1)*(y-y_1))

    Q_11=P_heater[row,col]
    Q_12=P_heater[row+1,col]
    Q_21=P_heater[row,col+1]
    Q_22=P_heater[row+1,col+1]
    P_heater=1/((x_2-x_1)*(y_2-y_1))*(Q_11*(x_2-x)*(y_2-y)+Q_21*(x-x_1)*(y_2-y)+Q_12*(x_2-x)*(y-y_1)+Q_22*(x-x_1)*(y-y_1))

    if F_pv==None:
   
        F_data=np.loadtxt('%s/post/%s/%s-%s-data_F_pv.csv'%(resdir, year, case, location), delimiter=',')
        F_pv=F_data[1:,1:]
        Q_11=F_pv[row,col]
        Q_12=F_pv[row+1,col]
        Q_21=F_pv[row,col+1]
        Q_22=F_pv[row+1,col+1]
        F_pv=1/((x_2-x_1)*(y_2-y_1))*(Q_11*(x_2-x)*(y_2-y)+Q_21*(x-x_1)*(y_2-y)+Q_12*(x_2-x)*(y-y_1)+Q_22*(x-x_1)*(y-y_1))

    P_load=500.e3 #kW
    pv_max=rm*P_load*F_pv # kW
    wind_max=rm*P_load*(1.-F_pv)
    TES_capa=P_load*sh

    return cf, P_heater, pv_max, wind_max, TES_capa  



def get_BAT_design(rm, sh, location, case, resdir, year=2020, F_pv=None):

    '''
    year (int): year basis of the design
    costmodel (str): '2020', '2030', '2050', '2020_ub', ''2020_lb'
    '''

    CF_data=np.loadtxt('%s/post/%s/%s-%s-data_CF.csv'%(resdir, year, case, location), delimiter=',')
    Pbat_data=np.loadtxt('%s/post/%s/%s-%s-data_P_bat.csv'%(resdir, year, case, location), delimiter=',')


    CF=CF_data[1:,1:]
    P_bat=Pbat_data[1:,1:]
    RM=CF_data[1:,0]
    SH=CF_data[0,1:]

    x=sh
    y=rm

    idx=np.argmin(abs(RM-rm))
    if RM[idx]!=1:
        row=idx-1
    else:
        row=idx

    idx=np.argmin(abs(SH-sh))
    if SH[idx]>0:
        col=idx-1
    else:
        col=idx

    x_1=SH[col]
    x_2=SH[col+1]
    y_1=RM[row]
    y_2=RM[row+1]
    Q_11=CF[row,col]
    Q_12=CF[row+1,col]
    Q_21=CF[row,col+1]
    Q_22=CF[row+1,col+1]
    cf=1/((x_2-x_1)*(y_2-y_1))*(Q_11*(x_2-x)*(y_2-y)+Q_21*(x-x_1)*(y_2-y)+Q_12*(x_2-x)*(y-y_1)+Q_22*(x-x_1)*(y-y_1))

    Q_11=P_bat[row,col]
    Q_12=P_bat[row+1,col]
    Q_21=P_bat[row,col+1]
    Q_22=P_bat[row+1,col+1]
    P_bat=1/((x_2-x_1)*(y_2-y_1))*(Q_11*(x_2-x)*(y_2-y)+Q_21*(x-x_1)*(y_2-y)+Q_12*(x_2-x)*(y-y_1)+Q_22*(x-x_1)*(y-y_1))

    if F_pv==None:
        F_data=np.loadtxt('%s/post/%s/%s-%s-data_F_pv.csv'%(resdir, year , case, location), delimiter=',')
        F_pv=F_data[1:,1:]

        Q_11=F_pv[row,col]
        Q_12=F_pv[row+1,col]
        Q_21=F_pv[row,col+1]
        Q_22=F_pv[row+1,col+1]
        F_pv=1/((x_2-x_1)*(y_2-y_1))*(Q_11*(x_2-x)*(y_2-y)+Q_21*(x-x_1)*(y_2-y)+Q_12*(x_2-x)*(y-y_1)+Q_22*(x-x_1)*(y-y_1))


    P_load=500.e3 #kW
    pv_max=rm*P_load*F_pv # kW
    wind_max=rm*P_load*(1.-F_pv)
    P_heater=P_load/0.99
    bat_capa=sh*P_heater
    bat_pmax=P_bat*1000.

    return cf, P_heater, pv_max, wind_max, bat_capa, bat_pmax

def get_PHES_design(rm, sh, location, case, resdir, year=2020, F_pv=None):

    '''
    year (int): year basis of the design
    costmodel (str): '2020', '2030', '2050', '2020_ub', ''2020_lb'
    '''

    CF_data=np.loadtxt('%s/post/%s/%s-%s-data_CF.csv'%(resdir, year, case, location), delimiter=',')
    PHES_data=np.loadtxt('%s/post/%s/%s-%s-data_P_PHES.csv'%(resdir, year, case, location), delimiter=',')

    CF=CF_data[1:,1:]
    P_PHES=PHES_data[1:,1:]
    RM=CF_data[1:,0]
    SH=CF_data[0,1:]

    x=sh
    y=rm

    idx=np.argmin(abs(RM-rm))
    if RM[idx]!=1:
        row=idx-1
    else:
        row=idx

    idx=np.argmin(abs(SH-sh))
    if SH[idx]>0:
        col=idx-1
    else:
        col=idx

    x_1=SH[col]
    x_2=SH[col+1]
    y_1=RM[row]
    y_2=RM[row+1]
    Q_11=CF[row,col]
    Q_12=CF[row+1,col]
    Q_21=CF[row,col+1]
    Q_22=CF[row+1,col+1]
    cf=1/((x_2-x_1)*(y_2-y_1))*(Q_11*(x_2-x)*(y_2-y)+Q_21*(x-x_1)*(y_2-y)+Q_12*(x_2-x)*(y-y_1)+Q_22*(x-x_1)*(y-y_1))

    Q_11=P_PHES[row,col]
    Q_12=P_PHES[row+1,col]
    Q_21=P_PHES[row,col+1]
    Q_22=P_PHES[row+1,col+1]
    P_PHES=1/((x_2-x_1)*(y_2-y_1))*(Q_11*(x_2-x)*(y_2-y)+Q_21*(x-x_1)*(y_2-y)+Q_12*(x_2-x)*(y-y_1)+Q_22*(x-x_1)*(y-y_1))

    if F_pv==None:
        F_data=np.loadtxt('%s/post/%s/%s-%s-data_F_pv.csv'%(resdir, year, case, location), delimiter=',')
        F_pv=F_data[1:,1:]

        Q_11=F_pv[row,col]
        Q_12=F_pv[row+1,col]
        Q_21=F_pv[row,col+1]
        Q_22=F_pv[row+1,col+1]
        F_pv=1/((x_2-x_1)*(y_2-y_1))*(Q_11*(x_2-x)*(y_2-y)+Q_21*(x-x_1)*(y_2-y)+Q_12*(x_2-x)*(y-y_1)+Q_22*(x-x_1)*(y-y_1))


    P_load=500.e3 #kW
    pv_max=rm*P_load*F_pv # kW
    wind_max=rm*P_load*(1.-F_pv)
    P_heater=P_load/0.99
    PHES_capa=sh*P_heater
    PHES_pmax=P_PHES*1000.

    return cf, P_heater, pv_max, wind_max, PHES_capa, PHES_pmax
