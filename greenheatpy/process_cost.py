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


def plot_reduction():

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
    plt.savefig(open('./future-cost-reductoin.png', 'wb'),  dpi=200, bbox_inches='tight')
    #plt.show()
    plt.close()


def update_cost(location, case, year, costmodel):
    '''
    location (str): location
    case (str): case name
    year (int): year of the design base
    costmodel (str): '2020', '2030', '2050', '2020_ub', ''2020_lb'
    '''

    resdir='./post'
    data=np.loadtxt('./post/%s/%s-%s-data_CF.csv'%(year, case, location), delimiter=',')

    RM=data[1:, 0]
    SH=data[0,1:]
    #SH, RM=np.meshgrid(t_storage, multiple)
    m=int(len(RM))
    n=int(len(SH))

    LCOH=np.array([])
    CF=np.array([])
    savedetails=True

    for rm in RM:
        for sh in SH:

            if savedetails:
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
    np.savetxt('./post/%s/%s-%s-data_LCOH.csv'%(costmodel, case, location), savedata, delimiter=',', fmt='%.2f') 
    savedata=np.vstack((SH, CF))
    savedata=np.hstack((np.append(0, RM).reshape(m+1, 1), savedata))
    np.savetxt('./post/%s/%s-%s-data_CF.csv'%(costmodel, case, location), savedata, delimiter=',', fmt='%.2f') 




'''
def get_cf_lcoh_optimal(location, case, year):

    resdir='./post'
    if 'HYBRID' in case:
        data=np.loadtxt('./post/%s/%s-%s-data_CF.csv'%(year, case, location), delimiter=',')
        LCOH=np.loadtxt('./post/%s/%s-%s-data_LCOH.csv'%(year, case, location), delimiter=',')
        LCOH=LCOH[1:,1:]
        CF=data[1:, 1:]  
        RM=data[1:, 0]
        SH=data[0,1:]
        #SH, RM=np.meshgrid(t_storage, multiple)
        m=int(len(RM))
        n=int(len(SH))
    else:
        data=np.loadtxt('./post/2020/%s-%s-data_CF.csv'%(case, location), delimiter=',')

        RM=data[1:, 0]
        SH=data[0,1:]
        #SH, RM=np.meshgrid(t_storage, multiple)
        m=int(len(RM))
        n=int(len(SH))

        LCOH=np.array([])
        CF=np.array([])
        savedetails=True
        for rm in RM:
            for sh in SH:
                if savedeails:
                    if case=='CST':
                        lcoh_1, cf_1=get_CST_design(rm, sh, location, case, resdir,  savename='CST-%s_%.3f_%.2f'%(location, rm, sh), year=year)
                    elif case=='CST-modular':
                        lcoh_1, cf_1=get_CST_modular_design(rm, sh, location, case, resdir,  savename='CST-modular-%s_%.3f_%.2f'%(location, rm, sh), year=year)
                    elif case=='TES-PV':
                        lcoh_1, cf_1=get_TES_design(rm, sh, location, case, resdir,  savename='TES-PV-%s_%.3f_%.2f'%(location, rm, sh), year=year, F_pv=1)
                    elif case=='TES-WIND':
                        lcoh_1, cf_1=get_TES_design(rm, sh, location, case, resdir,  savename='TES-WIND-%s_%.3f_%.2f'%(location, rm, sh), year=year, F_pv=0)
                    elif case=='TES-HYBRID':
                        lcoh_1, cf_1=get_TES_design(rm, sh, location, case, resdir,  savename='TES-HYBRID-%s_%.3f_%.2f'%(location, rm, sh), year=year, F_pv=None)
                    elif case=='BAT-PV':
                        lcoh_1, cf_1=get_BAT_design(rm, sh, location, case, resdir,  savename='BAT-PV-%s_%.3f_%.2f'%(location, rm, sh), year=year, F_pv=1)
                    elif case=='BAT-WIND':
                        lcoh_1, cf_1=get_BAT_design(rm, sh, location, case, resdir,  savename='BAT-WIND-%s_%.3f_%.2f'%(location, rm, sh), year=year, F_pv=0)
                    elif case=='BAT-HYBRID':
                        lcoh_1, cf_1=get_BAT_design(rm, sh, location, case, resdir,  savename='BAT-HYBRID-%s_%.3f_%.2f'%(location, rm, sh), year=year, F_pv=None)
                    elif case=='PHES-PV':
                        lcoh_1, cf_1=get_PHES_design(rm, sh, location, case, resdir,  savename='PHES-PV-%s_%.3f_%.2f'%(location, rm, sh), year=year, F_pv=1)
                    elif case=='PHES-WIND':
                        lcoh_1, cf_1=get_PHES_design(rm, sh, location, case, resdir,  savename='PHES-WIND-%s_%.3f_%.2f'%(location, rm, sh), year=year, F_pv=0)
                    elif case=='PHES-HYBRID':
                        lcoh_1, cf_1=get_PHES_design(rm, sh, location, case, resdir,  savename='PHES-HYBRID-%s_%.3f_%.2f'%(location, rm, sh), year=year, F_pv=None)

                else:
                    if case=='CST':
                        lcoh_1, cf_1=get_CST_design(rm, sh, location, case, resdir,  savename=None, year=year)
                    elif case=='CST-modular':
                        lcoh_1, cf_1=get_CST_modular_design(rm, sh, location, case, resdir,  savename=None, year=year)
                    elif case=='TES-PV':
                        lcoh_1, cf_1=get_TES_design(rm, sh, location, case, resdir,  savename=None, year=year, F_pv=1)
                    elif case=='TES-WIND':
                        lcoh_1, cf_1=get_TES_design(rm, sh, location, case, resdir,  savename=None, year=year, F_pv=0)
                    elif case=='TES-HYBRID':
                        lcoh_1, cf_1=get_TES_design(rm, sh, location, case, resdir,  savename=None, year=year, F_pv=None)
                    elif case=='BAT-PV':
                        lcoh_1, cf_1=get_BAT_design(rm, sh, location, case, resdir,  savename=None, year=year, F_pv=1)
                    elif case=='BAT-WIND':
                        lcoh_1, cf_1=get_BAT_design(rm, sh, location, case, resdir,  savename=None, year=year, F_pv=0)
                    elif case=='BAT-HYBRID':
                        lcoh_1, cf_1=get_BAT_design(rm, sh, location, case, resdir,  savename=None, year=year, F_pv=None)
                    elif case=='PHES-PV':
                        lcoh_1, cf_1=get_PHES_design(rm, sh, location, case, resdir,  savename=None, year=year, F_pv=1)
                    elif case=='PHES-WIND':
                        lcoh_1, cf_1=get_PHES_design(rm, sh, location, case, resdir,  savename=None, year=year, F_pv=0)
                    elif case=='PHES-HYBRID':
                        lcoh_1, cf_1=get_PHES_design(rm, sh, location, case, resdir,  savename=None, year=year, F_pv=None)

                LCOH=np.append(LCOH, lcoh_1)
                CF=np.append(CF, cf_1)

        LCOH=LCOH.reshape(m,n)
        CF=CF.reshape(m,n) 

        np.savetxt('./post/%s/%s-%s-data-LCOH.csv'%(year, case, location), LCOH, delimiter=',', fmt='%.2f') 
        #np.savetxt('./future-cost/%s-%s-%s-data-CF.csv'%(year, location, case), CF, delimiter=',', fmt='%.6f') 

    t_storage=SH
    multiple=RM
    SH, RM=np.meshgrid(SH, RM)
    fts=14
    levels=np.r_[30, 40, 50, 70, 80, 90, 95, 99]
    llabels=['%.0f%%'%l for l in levels]
    CS = plt.contour(t_storage, multiple, CF*100., levels, cmap='jet')

    results=np.array([])
    manual_locations=[]
    for a in range(len(levels)):
        L0=9999
        sh0=0
        rm0=0
        for b in range(len(CS.collections[a].get_paths())):
            p=CS.collections[a].get_paths()[b]
            v=p.vertices
            x=v[:,0]
            y=v[:,1]
            manual_locations.append((x[1], y[1]))
            for i in range(len(x)):
                sh=x[i]
                rm=y[i]
                
                idx=np.argmin(abs(multiple-rm))
                if multiple[idx]!=1:
                    row=idx-1
                else:
                    row=idx

                idx=np.argmin(abs(t_storage-sh))
                if t_storage[idx]>0:
                    col=idx-1
                else:
                    col=idx

                x_1=t_storage[col]
                x_2=t_storage[col+1]
                y_1=multiple[row]
                y_2=multiple[row+1]
                Q_11=LCOH[row,col]
                Q_12=LCOH[row+1,col]
                Q_21=LCOH[row,col+1]
                Q_22=LCOH[row+1,col+1]
                lcoh=1/((x_2-x_1)*(y_2-y_1))*(Q_11*(x_2-sh)*(y_2-rm)+Q_21*(sh-x_1)*(y_2-rm)+Q_12*(x_2-sh)*(rm-y_1)+Q_22*(sh-x_1)*(rm-y_1))                
                if lcoh<=L0:
                    L0=lcoh
                    sh0=sh
                    rm0=rm
        results=np.append(results, (levels[a], sh0, rm0, L0)) 
    
    results=results.reshape(int(len(results)/4), 4)   
    title=np.array(['CF','SH','RM','LCOH']).reshape(1,4)
    summary=np.vstack((title, results))
    np.savetxt('./post/%s/%s-%s-LCOH-CF.csv'%(year, case, location), summary, fmt='%s', delimiter=',')    



if __name__=='__main__':
    #plot_reduction()
    
    locations=[ 'Burnie']#, 'Pilbara', 'Pinjara',  'Upper Spencer Gulf',  'Gladstone']
    cases=[#'CST',
           #'CST-modular',
           #'TES-HYBRID', 
           #'TES-PV',
           #'TES-WIND',
           'BAT-HYBRID',
           #'BAT-PV',
           #'BAT-WIND',
           #'PHES-HYBRID',
           #'PHES-PV',
           #'PHES-WIND'
            ]
    year=2030
   
    for location in locations:
        for case in cases:
            #fn='./post/%s/%s-%s-LCOH-CF.csv'%(year, case, location)
            #if not os.path.exists(fn):
            get_cf_lcoh_optimal(location=location, case=case, year=year)
    
    for location in locations:
        plot_cf_lcoh_comparison(location, year=year)
'''    
