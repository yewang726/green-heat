from greenheatpy.parameters import Parameters
from greenheatpy.get_single_design import get_CST_design, get_CST_modular_design, get_TES_design, get_BAT_design,get_PHES_design
import os
import numpy as np
import matplotlib.pyplot as plt


def get_reduction_ratio(array, symbol, label):
    a=array[0]
    b=array[1]
    c=array[2]

    r1=b/a
    r2=c/b*r1
    if r1==0.8 and abs(r2-0.64)<1e-5:
        fixed=True
    else:
        fixed=False
    year=np.r_[2020, 2030, 2050]

    if not fixed:
        plt.plot(year, np.r_[1, r1, r2], symbol, label=label)
    else:
        plt.plot(year, np.r_[1, r1, r2], 'black', label=label)


def plot_reduction(resdir):

    fts=14
    pm=Parameters()


    c_site_cst=np.r_[pm.c_site_cst, pm.c_site_cst_2030, pm.c_site_cst_2050]
    c_land_cst=np.r_[pm.c_land_cst, pm.c_land_cst_2030, pm.c_land_cst_2050]
    c_recv_ref=np.r_[pm.C_recv_ref, pm.C_recv_ref_2030, pm.C_recv_ref_2050]
    c_tower_fix=np.r_[pm.C_tower_fix, pm.C_tower_fix_2030, pm.C_tower_fix_2050]
    c_helio=np.r_[pm.c_helio, pm.c_helio_2030, pm.c_helio_2050]
    c_pv_system=np.r_[pm.c_pv_system, pm.c_pv_system_2030, pm.c_pv_system_2050]
    c_wind_system=np.r_[pm.c_wind_system, pm.c_wind_system_2030, pm.c_wind_system_2050]
    c_bt_energy=np.r_[pm.c_bt_energy, pm.c_bt_energy_2030, pm.c_bt_energy_2050]
    c_bt_power=np.r_[pm.c_bt_power, pm.c_bt_power_2030, pm.c_bt_power_2050]
    c_PHES_energy=np.r_[pm.c_PHES_energy, pm.c_PHES_energy_2030, pm.c_PHES_energy_2050]
    c_PHES_power=np.r_[pm.c_PHES_power, pm.c_PHES_power_2030, pm.c_PHES_power_2050]
    c_TES=np.r_[pm.c_TES, pm.c_TES_2030, pm.c_TES_2050]
    c_heater=np.r_[pm.c_heater, pm.c_heater_2030, pm.c_heater_2050]

    get_reduction_ratio(c_site_cst, 'r-.', 'cst site')
    get_reduction_ratio(c_land_cst, 'r:', label='cst land')
    get_reduction_ratio(c_helio, 'r--', label='cst helios')
    get_reduction_ratio(c_recv_ref, 'r-', label='cst recv')
    get_reduction_ratio(c_tower_fix,'rx', label='cst tower')
    get_reduction_ratio(c_pv_system, 'g', label='pv')
    get_reduction_ratio(c_wind_system,'b', label='wind')
    get_reduction_ratio(c_bt_energy ,'y-', label='batt en')
    get_reduction_ratio( c_bt_power, 'y--', label='batt power')
    get_reduction_ratio(c_PHES_energy, 'p-',  label='PHES en')
    get_reduction_ratio(c_PHES_power , 'p--', label='PHES power')
    get_reduction_ratio(c_TES,'orange', label='TES')
    get_reduction_ratio(c_heater,'blueviolet', label='heater')


    plt.legend(loc=1, bbox_to_anchor=(1.5,1.), fontsize=fts)
    plt.xlabel('Year', fontsize=fts)
    plt.ylabel('Cost reduction rate', fontsize=fts)
    plt.xticks(np.arange(2020, 2060, 10), fontsize=fts)
    plt.yticks(fontsize=fts)
    plt.savefig(open('%s/future-cost-reductoin.png'%resdir, 'wb'),  dpi=200, bbox_inches='tight')
    #plt.show()
    plt.close()


def update_cost(location, case, year, costmodel, resdir, verbose=False):
    '''
    location (str): location
    case (str): case name
    year (int): year of the design base
    costmodel (str): '2020', '2030', '2050', '2020_ub', ''2020_lb'
    resdir (str): the main directory to deal with input and output 
    verbose (bool): to save the case design details or not
    '''

    data=np.loadtxt('%s/post/%s/%s-%s-data_CF.csv'%(resdir, year, case, location), delimiter=',')

    RM=data[1:, 0]
    SH=data[0,1:]
    m=int(len(RM))
    n=int(len(SH))

    LCOH=np.array([])
    CF=np.array([])

    for rm in RM:
        for sh in SH:

            if verbose:
                savename='%s-%s_%.3f_%.2f'%(case, location, rm, sh)
            else:
                savename=None

            if case=='CST':
                lcoh_1, cf_1=get_CST_design(rm, sh, location, case, resdir,  savename=savename, year=year, costmodel=costmodel)
            elif case=='CST-modular':
                lcoh_1, cf_1=get_CST_modular_design(rm, sh, location, case, resdir,  savename=savename, year=year, costmodel=costmodel)
            elif case=='TES-PV':
                lcoh_1, cf_1=get_TES_design(rm, sh, location, case, resdir,  savename=savename, year=year, F_pv=1, costmodel=costmodel)
            elif case=='TES-WIND':
                lcoh_1, cf_1=get_TES_design(rm, sh, location, case, resdir,  savename=savename, year=year, F_pv=0, costmodel=costmodel)
            elif case=='TES-HYBRID':
                lcoh_1, cf_1=get_TES_design(rm, sh, location, case, resdir,  savename=savename, year=year, F_pv=None, costmodel=costmodel)
            elif case=='BAT-PV':
                lcoh_1, cf_1=get_BAT_design(rm, sh, location, case, resdir,  savename=savename, year=year, F_pv=1, costmodel=costmodel)
            elif case=='BAT-WIND':
                lcoh_1, cf_1=get_BAT_design(rm, sh, location, case, resdir,  savename=savename, year=year, F_pv=0, costmodel=costmodel)
            elif case=='BAT-HYBRID':
                lcoh_1, cf_1=get_BAT_design(rm, sh, location, case, resdir,  savename=savename, year=year, F_pv=None, costmodel=costmodel)
            elif case=='PHES-PV':
                lcoh_1, cf_1=get_PHES_design(rm, sh, location, case, resdir,  savename=savename, year=year, F_pv=1, costmodel=costmodel)
            elif case=='PHES-WIND':
                lcoh_1, cf_1=get_PHES_design(rm, sh, location, case, resdir,  savename=savename, year=year, F_pv=0, costmodel=costmodel)
            elif case=='PHES-HYBRID':
                lcoh_1, cf_1=get_PHES_design(rm, sh, location, case, resdir,  savename=savename, year=year, F_pv=None, costmodel=costmodel)


            LCOH=np.append(LCOH, lcoh_1)
            CF=np.append(CF, cf_1)

    LCOH=LCOH.reshape(m,n)
    CF=CF.reshape(m,n) 

    savedata=np.vstack((SH, LCOH))
    savedata=np.hstack((np.append(0, RM).reshape(m+1, 1), savedata))
    np.savetxt('%s/post/%s/%s-%s-data_LCOH.csv'%(resdir, costmodel, case, location), savedata, delimiter=',', fmt='%.2f') 
    savedata=np.vstack((SH, CF))
    savedata=np.hstack((np.append(0, RM).reshape(m+1, 1), savedata))
    np.savetxt('%s/post/%s/%s-%s-data_CF.csv'%(resdir, costmodel, case, location), savedata, delimiter=',', fmt='%.2f') 

   
