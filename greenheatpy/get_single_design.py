'''
Get a specific design by interpolating the SH-RM data

'''

import numpy as np
from greenheatpy.parameters import Parameters, CST_SL_OM
from greenheatpy.master import cal_LCOH
from greenheatpy.projdirs import datadir
from greenheatpy.get_green_h2 import get_best_location

def get_CST_design(rm, sh, location, case, resdir, savename=None, year=2020, costmodel='2020', OM_method='SL'):


    CF_data=np.loadtxt('%s/2020/%s-%s-data_CF.csv'%(resdir, case, location), delimiter=',')
    Aland_data=np.loadtxt('%s/2020/%s-%s-data_Aland.csv'%(resdir, case, location), delimiter=',', skiprows=1)
    Drecv_data=np.loadtxt('%s/2020/%s-%s-data_Drecv.csv'%(resdir, case, location), delimiter=',', skiprows=1)
    Hrecv_data=np.loadtxt('%s/2020/%s-%s-data_Hrecv.csv'%(resdir, case, location), delimiter=',', skiprows=1)
    Htower_data=np.loadtxt('%s/2020/%s-%s-data_Htower.csv'%(resdir, case, location), delimiter=',', skiprows=1)
    Nhelio_data=np.loadtxt('%s/2020/%s-%s-data_Nhelio.csv'%(resdir, case, location), delimiter=',', skiprows=1)

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

    pm=Parameters()
    if costmodel=='2020':
        C_recv = pm.C_recv_ref * ( H_recv * D_recv * np.pi / pm.A_recv_ref)**pm.f_recv_exp
        C_tower = pm.C_tower_fix * np.exp(pm.f_tower_exp * (H_tower - H_recv/2.+pm.H_helio/2.))
        C_field = pm.c_helio * n_helios * pm.A_helio
        C_site = pm.c_site_cst * pm.A_helio * n_helios
        C_TES = pm.c_TES * TES_capa
        C_land = pm.c_land_cst * A_land
    elif costmodel=='2030':
        C_recv = pm.C_recv_ref_2030 * ( H_recv * D_recv * np.pi / pm.A_recv_ref)**pm.f_recv_exp
        C_tower = pm.C_tower_fix_2030 * np.exp(pm.f_tower_exp * (H_tower - H_recv/2.+pm.H_helio/2.))
        C_field = pm.c_helio_2030 * n_helios * pm.A_helio
        C_site = pm.c_site_cst_2030 * pm.A_helio * n_helios
        C_TES = pm.c_TES_2030 * TES_capa
        C_land = pm.c_land_cst_2030 * A_land

    elif costmodel=='2050':
        C_recv = pm.C_recv_ref_2050 * ( H_recv * D_recv * np.pi / pm.A_recv_ref)**pm.f_recv_exp
        C_tower = pm.C_tower_fix_2050 * np.exp(pm.f_tower_exp * (H_tower - H_recv/2.+pm.H_helio/2.))
        C_field = pm.c_helio_2050 * n_helios * pm.A_helio
        C_site = pm.c_site_cst_2050 * pm.A_helio * n_helios
        C_TES = pm.c_TES_2050 * TES_capa
        C_land = pm.c_land_cst_2050 * A_land

    else:
        print('Year %s data is not implemented'%year)

    CAPEX = C_recv + C_tower + C_field + C_site + C_TES 

    C_direct= CAPEX*(1.+pm.r_conting_cst)
    C_indirect = pm.r_EPC_owner*C_direct + C_land 
    C_cap=C_direct + C_indirect


    if OM_method=='SAM':
        OM_fixed=pm.c_om_cst_fix * P_load_des
        c_OM_var = pm.c_om_cst_var
    elif OM_method=='SL':
        A_helios=n_helios * pm.A_helio
        OM_fixed=CST_SL_OM(A_helios)
        c_OM_var=0 

    LCOH, epy, OM_total=cal_LCOH(CF,  P_load, C_cap, OM_fixed, c_OM_var, r_discount=pm.r_disc_real, t_life=pm.t_life, t_cons=pm.t_constr_cst)

    summary=np.array([
            ['SM',rm, '-'],
            ['t_storage', sh, 'h'],
            ['LCOH', LCOH, 'USD/MWh_th'],
            ['CF', CF, '-'],
            ['H_recv', H_recv, 'm'],
            ['D_recv', D_recv, 'm'],
            ['H_tower', H_tower, 'm'],
            ['n_helios', n_helios, '-'],
            ['A_land', A_land, 'm2'],
            ['TES_capa',TES_capa/1e3, 'MWh'],
            ['EPY', epy, 'MWh'],
            ['C_cap_tot', C_cap/1e6, 'M.USD'],
            ['OM_tot', OM_total/1e6, 'M.USD'],
            ['C_recv', C_recv/1e6, 'M.USD'],
            ['C_tower', C_tower/1e6, 'M.USD'],
            ['C_field', C_field/1e6, 'M.USD'],
            ['C_site', C_site/1e6, 'M.USD'],
            ['C_TES', C_TES/1e6, 'M.USD'],
            ['C_land', C_land/1e6, 'M.USD'],
            ['C_equipment', CAPEX/1e6, 'M.USD'],
            ['C_direct', C_direct/1e6, 'M.USD'],
            ['C_indirect', C_indirect/1e6, 'USD'],
            ['r_real_discount', pm.r_disc_real, '-'],
            ['t_construction', pm.t_constr_cst, 'year'],
            ['t_life', pm.t_life, 'year'],
    ])

    if savename!=None:
        np.savetxt('./summary_%s.csv'%(savename), summary, fmt='%s', delimiter=',')
    print('%s RM=%.1f, SH=%.1f, CF=%.4f, LCOH=%.2f'%(case, rm, sh, CF, LCOH))	
    return LCOH, CF

def get_CST_modular_design(rm, sh, location, case, resdir, savename=None, year=2020, costmodel='2020', OM_method='SL'):

    CF_data=np.loadtxt('%s/2020/%s-%s-data_CF.csv'%(resdir, case, location), delimiter=',')
    num_modules=np.loadtxt('%s/2020/%s-%s-data_num_modules.csv'%(resdir, case, location), delimiter=',', skiprows=1)


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

    pm=Parameters()
    if costmodel=='2020':
        C_recv = pm.C_recv_ref * ( H_recv * D_recv * np.pi / pm.A_recv_ref)**pm.f_recv_exp*num_modules
        C_tower = pm.C_tower_fix * np.exp(pm.f_tower_exp * (H_tower - H_recv/2.+pm.H_helio/2.))*num_modules
        C_field = pm.c_helio * n_helios * pm.A_helio*num_modules
        C_site = pm.c_site_cst * pm.A_helio * n_helios*num_modules
        C_TES = pm.c_TES * TES_capa
        C_land = pm.c_land_cst * A_land*num_modules
    elif costmodel=='2030':
        C_recv = pm.C_recv_ref_2030 * ( H_recv * D_recv * np.pi / pm.A_recv_ref)**pm.f_recv_exp*num_modules
        C_tower = pm.C_tower_fix_2030 * np.exp(pm.f_tower_exp * (H_tower - H_recv/2.+pm.H_helio/2.))*num_modules
        C_field = pm.c_helio_2030 * n_helios * pm.A_helio*num_modules
        C_site = pm.c_site_cst_2030 * pm.A_helio * n_helios*num_modules
        C_TES = pm.c_TES_2030 * TES_capa
        C_land = pm.c_land_cst_2030 * A_land*num_modules
    
    elif costmodel=='2050':
        C_recv = pm.C_recv_ref_2050 * ( H_recv * D_recv * np.pi / pm.A_recv_ref)**pm.f_recv_exp*num_modules
        C_tower = pm.C_tower_fix_2050 * np.exp(pm.f_tower_exp * (H_tower - H_recv/2.+pm.H_helio/2.))*num_modules
        C_field = pm.c_helio_2050 * n_helios * pm.A_helio*num_modules
        C_site = pm.c_site_cst_2050 * pm.A_helio * n_helios*num_modules
        C_TES = pm.c_TES_2050 * TES_capa
        C_land = pm.c_land_cst_2050 * A_land*num_modules

    else:
        print('Year %s data is not implemented'%year)

    CAPEX = C_recv + C_tower + C_field + C_site + C_TES 

    C_direct= CAPEX*(1.+pm.r_conting_cst)
    C_indirect = pm.r_EPC_owner*C_direct + C_land 
    C_cap=C_direct + C_indirect


    if OM_method=='SAM':
        OM_fixed=pm.c_om_cst_fix * P_load_des
        c_OM_var = pm.c_om_cst_var
    elif OM_method=='SL':
        A_helios=n_helios * pm.A_helio
        OM_fixed=CST_SL_OM(A_helios)
        c_OM_var=0 

    LCOH, epy, OM_total=cal_LCOH(CF,  P_load, C_cap, OM_fixed, c_OM_var, r_discount=pm.r_disc_real, t_life=pm.t_life, t_cons=pm.t_constr_cst)

    summary=np.array([
            ['SM',rm, '-'],
            ['t_storage', sh, 'h'],
            ['LCOH', LCOH, 'USD/MWh_th'],
            ['CF', CF, '-'],
            ['H_recv', H_recv, 'm'],
            ['D_recv', D_recv, 'm'],
            ['H_tower', H_tower, 'm'],
            ['n_helios', n_helios, '-'],
            ['A_land', A_land, 'm2'],
            ['TES_capa',TES_capa/1e3, 'MWh'],
            ['EPY', epy, 'MWh'],
            ['C_cap_tot', C_cap/1e6, 'M.USD'],
            ['OM_tot', OM_total/1e6, 'M.USD'],
            ['C_recv', C_recv/1e6, 'M.USD'],
            ['C_tower', C_tower/1e6, 'M.USD'],
            ['C_field', C_field/1e6, 'M.USD'],
            ['C_site', C_site/1e6, 'M.USD'],
            ['C_TES', C_TES/1e6, 'M.USD'],
            ['C_land', C_land/1e6, 'M.USD'],
            ['C_equipment', CAPEX/1e6, 'M.USD'],
            ['C_direct', C_direct/1e6, 'M.USD'],
            ['C_indirect', C_indirect/1e6, 'USD'],
            ['r_real_discount', pm.r_disc_real, '-'],
            ['t_construction', pm.t_constr_cst, 'year'],
            ['t_life', pm.t_life, 'year'],
            ['num_modules', num_modules, '-'],
    ])

    if savename!=None:
        np.savetxt('./summary_%s.csv'%(savename), summary, fmt='%s', delimiter=',')
    print('%s RM=%.1f, SH=%.1f, CF=%.4f, LCOH=%.2f'%(case, rm, sh, CF, LCOH))	
    return LCOH, CF

def get_TES_design(rm, sh, location, case,  resdir, savename=None, year=2020, costmodel='2020', F_pv=None):
    '''
    year (int): year basis of the design
    costmodel (str): '2020', '2030', '2050', '2020_ub', ''2020_lb'
    '''

    CF_data=np.loadtxt('%s/%s/%s-%s-data_CF.csv'%(resdir, year, case, location), delimiter=',')
    Pheater_data=np.loadtxt('%s/%s/%s-%s-data_P_heater.csv'%(resdir, year, case, location), delimiter=',')


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
   
        F_data=np.loadtxt('%s/%s/%s-%s-data_F_pv.csv'%(resdir, year, case, location), delimiter=',')
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

    pm=Parameters()

    if costmodel =='2020':
        C_pv=pm.c_pv_system*pv_max
        C_wind=pm.c_wind_system*wind_max
        C_heater=P_heater*pm.c_heater*1000.
        C_TES=TES_capa*pm.c_TES

    elif costmodel =='2030':
        C_pv=pm.c_pv_system_2030*pv_max
        C_wind=pm.c_wind_system_2030*wind_max
        C_heater=P_heater*pm.c_heater_2030*1000.
        C_TES=TES_capa*pm.c_TES_2030

    elif costmodel =='2050':
        C_pv=pm.c_pv_system_2050*pv_max
        C_wind=pm.c_wind_system_2050*wind_max
        C_heater=P_heater*pm.c_heater_2050*1000.
        C_TES=TES_capa*pm.c_TES_2050

    else:
        print('Year %s data is not implemented'%year)



    CAPEX=C_pv+C_wind+C_heater+C_TES

    # heater replacement
    C_replace_heater=P_heater*pm.c_replace_heater*1000.
    n_replace_heater=int(pm.t_life/pm.t_life_heater)
    C_replc_heater_NPV=0
    for i in range(n_replace_heater):
        t=(i+1)*pm.t_life_heater+pm.t_constr_pv
        C_replc_heater_NPV+=C_replace_heater/(1+pm.r_disc_real)**t

    C_replace_NPV=C_replc_heater_NPV

    C_cap=CAPEX*(1+pm.r_conting_pv)+C_replace_NPV

    OM_fixed=pm.c_om_pv_fix*pv_max+pm.c_om_wind_fix*wind_max
    c_OM_var = 0.

    LCOH, epy, OM_total=cal_LCOH(cf,  P_load, C_cap, OM_fixed, c_OM_var, r_discount=pm.r_disc_real, t_life=pm.t_life, t_cons=pm.t_constr_pv)

    print('%s RM=%.1f, SH=%.1f, F_pv=%.3f, P_heater=%.1f (MW), CF=%.4f, LCOH=%.2f'%(case, rm, sh,  F_pv, P_heater, cf, LCOH))	


    summary=np.array([
            ['RM',rm, '-'],
            ['t_storage', sh, 'h'],
            ['LCOH', LCOH, 'USD/MWh_th'],
            ['CF', cf, '-'],
            ['r_pv', F_pv, '-'],
            ['pv_max', pv_max/1e3, 'MW'],
            ['wind_max', wind_max/1e3, 'MW'],
            ['P_heater',P_heater/1e3, 'MW'],
            ['TES_capa',TES_capa/1e3, 'MWh'],
            ['EPY', epy, 'MWh'],
            ['C_cap_tot', C_cap/1e6, 'M.USD'],
            ['OM_tot', OM_total/1e6, 'M.USD'],
            ['C_equipment', CAPEX/1e6, 'M.USD'],
            ['C_pv', C_pv/1e6, 'M.USD'],            
            ['C_wind', C_wind/1e6, 'M.USD'],  
            ['C_TES', C_TES/1e6, 'M.USD'],  
            ['C_heater', C_heater/1e6, 'M.USD'],  
            ['C_replace_heater_NPV', C_replc_heater_NPV/1e6, 'M.USD'],  
            ['C_replace_NPV', C_replace_NPV/1e6, 'M.USD'],  
            ['r_real_discount', pm.r_disc_real, '-'],
            ['t_construction', pm.t_constr_pv, 'year'],
            ['t_life', pm.t_life, 'year'],
            ['Location', location, '-']                   
    ])

    if savename!=None:
        np.savetxt('./summary_%s.csv'%(savename), summary, fmt='%s', delimiter=',')
    return LCOH, cf


def get_BAT_design(rm, sh, location, case, resdir, savename=None, year=2020, costmodel='2020', F_pv=None):

    '''
    year (int): year basis of the design
    costmodel (str): '2020', '2030', '2050', '2020_ub', ''2020_lb'
    '''

    CF_data=np.loadtxt('%s/%s/%s-%s-data_CF.csv'%(resdir, year, case, location), delimiter=',')
    Pbat_data=np.loadtxt('%s/%s/%s-%s-data_P_bat.csv'%(resdir, year, case, location), delimiter=',')


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
        F_data=np.loadtxt('%s/%s/%s-%s-data_F_pv.csv'%(resdir, year , case, location), delimiter=',')
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

    pm=Parameters()
    if costmodel =='2020':
        C_pv=pm.c_pv_system*pv_max
        C_wind=pm.c_wind_system*wind_max
        C_heater=P_heater*pm.c_heater
        C_bat=bat_capa*pm.c_bt_energy+bat_pmax*pm.c_bt_power

    elif costmodel =='2030':
        C_pv=pm.c_pv_system_2030*pv_max
        C_wind=pm.c_wind_system_2030*wind_max
        C_heater=P_heater*pm.c_heater_2030
        C_bat=bat_capa*pm.c_bt_energy_2030+bat_pmax*pm.c_bt_power_2030

    elif costmodel =='2050':
        C_pv=pm.c_pv_system_2050*pv_max
        C_wind=pm.c_wind_system_2050*wind_max
        C_heater=P_heater*pm.c_heater_2050
        C_bat=bat_capa*pm.c_bt_energy_2050+bat_pmax*pm.c_bt_power_2050

    else:
        print('Year %s data is not implemented'%year)


    CAPEX=C_pv+C_wind+C_heater+C_bat

    # heater replacement
    C_replace_heater=P_heater*pm.c_replace_heater
    n_replace_heater=int(pm.t_life/pm.t_life_heater)

    # battery replacement
    C_replace_bt=bat_capa*pm.c_replace_bt
    n_replace_bt=int(pm.t_life/pm.t_life_bt)

    C_replc_heater_NPV=0
    for i in range(n_replace_heater):
        t=(i+1)*pm.t_life_heater+pm.t_constr_pv
        C_replc_heater_NPV+=C_replace_heater/(1+pm.r_disc_real)**t

    C_replc_bt_NPV=0
    for i in range(n_replace_bt):
        t=(i+1)*pm.t_life_bt+pm.t_constr_pv
        C_replc_bt_NPV+=C_replace_bt/(1+pm.r_disc_real)**t

    C_replace_NPV=C_replc_heater_NPV+C_replc_bt_NPV

    C_cap=CAPEX*(1+pm.r_conting_pv)+C_replace_NPV

    OM_fixed=pm.c_om_pv_fix*pv_max+pm.c_om_wind_fix*wind_max
    c_OM_var = 0.

    LCOH, epy, OM_total=cal_LCOH(cf,  P_load, C_cap, OM_fixed, c_OM_var, r_discount=pm.r_disc_real, t_life=pm.t_life, t_cons=pm.t_constr_pv)

    print('%s RM=%.1f, SH=%.1f, F_pv=%.3f, P_bat=%.1f (MW), CF=%.4f, LCOH=%.2f'%(case, rm, sh,  F_pv, bat_pmax/1e3, cf, LCOH))	


    summary=np.array([
            ['RM',rm, '-'],
            ['t_storage', sh, 'h'],
            ['LCOH', LCOH, 'USD/MWh_th'],
            ['CF', cf, '-'],
            ['F_pv', F_pv, '-'],
            ['pv_max', pv_max/1e3, 'MW'],
            ['wind_max', wind_max/1e3, 'MW'],
            ['P_heater',P_heater/1e3, 'MW'],
            ['bat_capa',bat_capa/1e3, 'MWh'],
            ['bat_pmax',bat_pmax/1e3, 'MW'],
            ['EPY', epy, 'MWh'],
            ['C_cap_tot', C_cap/1e6, 'M.USD'],
            ['OM_tot', OM_total/1e6, 'M.USD'],
            ['C_equipment', CAPEX/1e6, 'M.USD'],
            ['C_pv', C_pv/1e6, 'M.USD'],            
            ['C_wind', C_wind/1e6, 'M.USD'],  
            ['C_bat', C_bat/1e6, 'M.USD'],  
            ['C_heater', C_heater/1e6, 'M.USD'],  
            ['C_replace_heater_NPV', C_replc_heater_NPV/1e6, 'M.USD'],  
            ['C_replace_bt_NPV', C_replc_bt_NPV/1e6, 'M.USD'],  
            ['C_replace_NPV', C_replace_NPV/1e6, 'M.USD'],  
            ['r_real_discount', pm.r_disc_real, '-'],
            ['t_construction', pm.t_constr_pv, 'year'],
            ['t_life', pm.t_life, 'year'],
            ['Location', location, '-']                 
    ])

    if savename!=None:
        np.savetxt('./summary_%s.csv'%savename, summary, fmt='%s', delimiter=',')

    return LCOH, cf


def get_PHES_design(rm, sh, location, case, resdir, savename=None, year=2020, costmodel='2020', F_pv=None):

    '''
    year (int): year basis of the design
    costmodel (str): '2020', '2030', '2050', '2020_ub', ''2020_lb'
    '''

    CF_data=np.loadtxt('%s/%s/%s-%s-data_CF.csv'%(resdir, year, case, location), delimiter=',')
    PHES_data=np.loadtxt('%s/%s/%s-%s-data_P_PHES.csv'%(resdir, year, case, location), delimiter=',')

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
        F_data=np.loadtxt('%s/%s/%s-%s-data_F_pv.csv'%(resdir, year, case, location), delimiter=',')
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

    pm=Parameters()
    if costmodel =='2020':
        C_pv=pm.c_pv_system*pv_max
        C_wind=pm.c_wind_system*wind_max
        C_heater=P_heater*pm.c_heater
        C_PHES=PHES_capa*pm.c_PHES_energy+PHES_pmax*pm.c_PHES_power

    elif costmodel =='2030':
        C_pv=pm.c_pv_system_2030*pv_max
        C_wind=pm.c_wind_system_2030*wind_max
        C_heater=P_heater*pm.c_heater_2030
        C_PHES=PHES_capa*pm.c_PHES_energy_2030+PHES_pmax*pm.c_PHES_power_2030

    elif costmodel =='2050':
        C_pv=pm.c_pv_system_2050*pv_max
        C_wind=pm.c_wind_system_2050*wind_max
        C_heater=P_heater*pm.c_heater_2050
        C_PHES=PHES_capa*pm.c_PHES_energy_2030+PHES_pmax*pm.c_PHES_power_2050

    else:
        print('Year %s data is not implemented'%year)


    CAPEX=C_pv+C_wind+C_heater+C_PHES

    # heater replacement
    C_replace_heater=P_heater*pm.c_replace_heater
    n_replace_heater=int(pm.t_life/pm.t_life_heater)

 
    C_replc_heater_NPV=0
    for i in range(n_replace_heater):
        t=(i+1)*pm.t_life_heater+pm.t_constr_pv
        C_replc_heater_NPV+=C_replace_heater/(1+pm.r_disc_real)**t


    C_replace_NPV=C_replc_heater_NPV

    C_cap=CAPEX*(1+pm.r_conting_pv)+C_replace_NPV

    OM_fixed=pm.c_om_pv_fix*pv_max+pm.c_om_wind_fix*wind_max+pm.c_om_PHES_fix*PHES_pmax
    c_OM_var = 0.

    LCOH, epy, OM_total=cal_LCOH(cf,  P_load, C_cap, OM_fixed, c_OM_var, r_discount=pm.r_disc_real, t_life=pm.t_life, t_cons=pm.t_constr_pv)

    print('%s RM=%.1f, SH=%.1f, F_pv=%.3f, P_PHES=%.1f (MW), CF=%.4f, LCOH=%.2f'%(case, rm, sh,  F_pv, PHES_pmax/1e3, cf, LCOH))	


    summary=np.array([
            ['RM',rm, '-'],
            ['t_storage', sh, 'h'],
            ['LCOH', LCOH, 'USD/MWh_th'],
            ['CF', cf, '-'],
            ['F_pv', F_pv, '-'],
            ['pv_max', pv_max/1e3, 'MW'],
            ['wind_max', wind_max/1e3, 'MW'],
            ['P_heater',P_heater/1e3, 'MW'],
            ['PHES_capa',PHES_capa/1e3, 'MWh'],
            ['PHES_pmax',PHES_pmax/1e3, 'MW'],
            ['EPY', epy, 'MWh'],
            ['C_cap_tot', C_cap/1e6, 'M.USD'],
            ['OM_tot', OM_total/1e6, 'M.USD'],
            ['C_equipment', CAPEX/1e6, 'M.USD'],
            ['C_pv', C_pv/1e6, 'M.USD'],            
            ['C_wind', C_wind/1e6, 'M.USD'],  
            ['C_PHES', C_PHES/1e6, 'M.USD'],  
            ['C_heater', C_heater/1e6, 'M.USD'],  
            ['C_replace_heater_NPV', C_replc_heater_NPV/1e6, 'M.USD'],  
            ['C_replace_NPV', C_replace_NPV/1e6, 'M.USD'],  
            ['r_real_discount', pm.r_disc_real, '-'],
            ['t_construction', pm.t_constr_pv, 'year'],
            ['t_life', pm.t_life, 'year'],
            ['Location', location, '-']                 
    ])

    if savename!=None:
        np.savetxt('./summary_%s.csv'%savename, summary, fmt='%s', delimiter=',')

    return LCOH, cf










