from solartherm import simulation
import DyMat
import numpy as np
import os
from greenheatpy.parameters import Parameters
from greenheatpy.master import cal_LCOH
from greenheatpy.gen_motab_data import gen_ref_power
import time
import functools
from scipy import optimize as sciopt

def objective_function(location, year, sim, t_storage, RM, obj_cf, par_n, par_v):

    nv=len(par_n)
    for i in range(nv):
        if par_n[i]=='r_pv':
            r_pv=par_v[i]
        elif par_n[i]=='P_heater':
            P_heater=par_v[i]
        elif par_n[i]=='P_ST_max':
            P_ST_max=par_v[i]
        elif par_n[i]=='RM':
            RM=par_v[i]
        elif par_n[i]=='t_storage':
            t_storage=par_v[i]

    var_n=['t_storage','RM','F_pv','P_ST_max']
    var_v=[str(t_storage), str(RM), str(r_pv), str(P_ST_max)]

    try:
        sim.update_pars(var_n, var_v)
        sim.simulate(start='0', stop='1y', step='5m', initStep=None, maxStep='5m', integOrder='1e-06', solver='dassl', nls='homotopy', lv='-LOG_SUCCESS,-stdout')
        res_fn=sim.res_fn
        res=DyMat.DyMatFile(res_fn)

        LCOH=process_BAT(res, year, obj_cf=obj_cf, verbose=True) 

    except:
        LCOH=99999

    return LCOH

def objective_function_PHES(location, year, sim, t_storage, RM, obj_cf, par_n, par_v):

    nv=len(par_n)
    for i in range(nv):
        if par_n[i]=='r_pv':
            r_pv=par_v[i]
        elif par_n[i]=='P_heater':
            P_heater=par_v[i]
        elif par_n[i]=='P_ST_max':
            P_ST=par_v[i]
        elif par_n[i]=='RM':
            RM=par_v[i]
        elif par_n[i]=='t_storage':
            t_storage=par_v[i]

    try:
        pm=Parameters()
        var_n=['t_storage','RM','F_pv','P_ST_max', 'eff_ST_roundtrip']
        var_v=[str(t_storage), str(RM), str(r_pv), str(P_ST), str(pm.eff_rdtrip_PHES)]
        sim.update_pars(var_n, var_v)
        sim.simulate(start='0', stop='1y', step='5m', initStep=None, maxStep='5m', integOrder='1e-06', solver='dassl', nls='homotopy', lv='-LOG_SUCCESS,-stdout')
        res_fn=sim.res_fn
        res=DyMat.DyMatFile(res_fn)

        LCOH=process_PHES(res, year, obj_cf=obj_cf, verbose=True) 
    except:
        LCOH=99999

    return LCOH

def objective_function_TES(location, year, sim, t_storage, RM, obj_cf, par_n, par_v):

    nv=len(par_n)
    for i in range(nv):
        if par_n[i]=='r_pv':
            r_pv=par_v[i]
        elif par_n[i]=='P_heater':
            P_heater=par_v[i]
        elif par_n[i]=='P_bat':
            P_bat=par_v[i]
        elif par_n[i]=='RM':
            RM=par_v[i]
        elif par_n[i]=='t_storage':
            t_storage=par_v[i]

    var_n=['t_storage','RM','F_pv','P_heater_max']
    var_v=[str(t_storage), str(RM), str(r_pv), str(P_heater)]
    try:
        sim.update_pars(var_n, var_v)
        sim.simulate(start='0', stop='1y', step='5m', initStep=None, maxStep='5m', integOrder='1e-06', solver='dassl', nls='homotopy', lv='-LOG_SUCCESS,-stdout')
        res_fn=sim.res_fn
        res=DyMat.DyMatFile(res_fn)
        LCOH=process_TES(res, year, obj_cf=obj_cf, verbose=True) 
    except:
        LCOH=99999

    return LCOH

def st_sciopt(mofn, location, t_storage, RM, method, LB, UB, nominals, names, casedir, case='BAT', year=2020, obj_cf=None, solcast_TMY=False):
    '''
    Arguments:
        model_name (str)  : minizic model name
        location   (str)  : site location
        t_storage         (float): storage hour (h)
        RM         (float): renewable multiple, the total size of the renewable energy collection system (e.g. PV+Wind) to the load   
        method     (str)  : the optimisation algorithm that is available in scipy package
                    e.g. 'Nelder-Mead', 'COBYLA', 'SLSQP', 'TNC', 
                        'L-BFGS-B' (can be used for maximisation)
        LB         (list) : lower bounds of all the variables
        UB         (list) : upper bounds of all the variables
        nominals   (list) : nominal values of all the variables
        names      (list) : names of all the variables
        casedir    (str)  : directory to save the restuls
        case       (str)  : 'TES', 'BAT' or 'PHES' 
        obj_cf     (float): None or the capacity factor that is aimed for
        solcast_TMY (bool): True to use solcast_TMY data, False to use the data in data/weather folder (from Windlab)
        
    Return:
        The LCOH minimised design
    '''
    start=time.time()
    cwd=os.getcwd()
    if not os.path.exists(casedir):
        os.makedirs(casedir)
    wd=os.path.abspath(casedir)
    os.chdir(casedir)

    model=os.path.splitext(os.path.split(mofn)[1])[0] 
    sim=simulation.Simulator(fn=mofn, fusemount=False)
    if not os.path.exists(model):
        print('compile model')
        sim.compile_model()
        sim.compile_sim(args=['-s'])
    print('finish compile')
    #sim.compile_model()
    #sim.compile_sim(args=['-s'])

    pv_fn=gen_ref_power(model_name='pv', location=location,  casedir=wd, plot=False, solcast_TMY=solcast_TMY)
    table_file_pv=pv_fn
    wind_fn=gen_ref_power(model_name='wind', location=location, casedir=wd, plot=False, solcast_TMY=solcast_TMY) 
    table_file_wind=wind_fn
    sim.update_pars(['table_file_pv', 'table_file_wind'], [table_file_pv, table_file_wind])

    bounds=[]
    nv=len(nominals)
    for i in range(nv):
        bounds.append([LB[i], UB[i]])        

    if case=='BAT':
        objfunc = functools.partial(objective_function, location, year,sim, t_storage, RM, obj_cf, names)
    elif case=='TES':
        objfunc = functools.partial(objective_function_TES,  location, year, sim, t_storage, RM, obj_cf, names)
    elif case=='PHES':
        objfunc = functools.partial(objective_function_PHES, location, year, sim, t_storage, RM, obj_cf, names)

    res = sciopt.minimize(objfunc, nominals, method=method, bounds=bounds,
			options={
				'disp': True,
			})

    print("")
    print('-----------')
    print('results',res)
    print('-----------')
    print("")
    #cand = [scale[i]*v + offset[i] for i, v in enumerate(res.x)]
    end=time.time()
    total_time=end-start # s
    print('Total time %.2f (s)'%total_time)
    os.chdir(cwd)
    return res.fun, res.x


def gen_dakota_input(mofn, system, obj_cf, var_names, nominals, lbs, ubs, num_eval=2400):
    
    dkt_in='''
        # Dakota Input File: sample.in
        # Usage:
        #    dakota -i sample.in -o sample.out > sample.stdout
        # or if run in multi-level parallelism:
        #    mpirun dakota -i sample.in -o sample.out > sample.stdout
        #    or
        #	 mpexec dakota -i sample.in -o sample.out > sample.stdout

		environment
			tabular_data
			tabular_data_file = "sample.dat"

		model
			single

		interface
			fork
			analysis_drivers = "interface_bb.py"
			parameters_file = "params.in"
			results_file = "results.out"
			file_tag 
			#file_save 	

		responses
			objective_functions = 1
			no_gradients
			no_hessians	

		method
		    soga
            seed = 10983
            max_function_evaluations = %s
            initialization_type unique_random
            population_size= 48		
            crossover_type 
                multi_point_parameterized_binary= 2
                crossover_rate = 0.8
            mutation_type replace_uniform
            mutation_rate = 0.2
            fitness_type merit_function
            replacement_type elitist
            convergence_type average_fitness_tracker
            percent_change = 0.05 num_generations = 100
            final_solutions = 3
            output silent


		variables 
	        discrete_state_set
            string 3
            set_values  "%s"  "%s" "%s" 
            descriptors  "fn"  "system" "obj_cf"  


        ''' %(num_eval, mofn, system, obj_cf) 

    var_num=int(len(var_names))	    
    m=''		
    m+='    continuous_design=%s\n'%var_num
    m+='        		initial_point'		
    for i in range(var_num):
        m+=' %s'%nominals[i]
    m+='\n'    
    m+='        		lower_bounds'	
    for i in range(var_num):
        m+=' %s'%lbs[i]
    m+='\n' 
    m+='        		upper_bounds'	
    for i in range(var_num):
        m+=' %s'%ubs[i]
    m+='\n' 		
    m+='        		descriptors'	
    for i in range(var_num):
        m+=' "%s"'%var_names[i]
    m+='\n' 						
        
    dkt_in+=m

    with open('sample.in', 'w') as f:
        f.write(dkt_in)		



def gen_interface_bb(model_name, location):
    '''
    This function generate the interface_bb.py file in the casedir
    which will be excuted by DAKOTA	
    '''

    bb='''#!/usr/bin/env python3
# Dakota will execute this python script
# The command line arguments will be extracted by the interface automatically.

import dakota.interfacing as di	
import os
import DyMat
from greenheatpy.optimisation_so_modelica import process_BAT, process_PHES, process_TES
from greenheatpy.parameters import Parameters
params, results = di.read_parameters_file()			
names=params.descriptors
fn=params.__getitem__("fn") #the modelica file
system=params.__getitem__("system") # BAT, PHES or TES
obj_cf=params.__getitem__("obj_cf") 
model=os.path.splitext(os.path.split(fn)[1])[0] # model name

obj_cf = None if obj_cf == 'None' else float(obj_cf)


var_n=[]
var_v=[]
for n in names[:-3]:

    print('variable   : ', n, '=', params.__getitem__(n))
    var_n.append(str(n))
    var_v.append(str(params.__getitem__(n)))

if 'PHES' in system:
    pm=Parameters()
    eff_ST_roundtrip=str(pm.eff_rdtrip_PHES)
    var_n.append("eff_ST_roundtrip")
    var_v.append(eff_ST_roundtrip)

if 'PV' in system:
    var_n.append("F_pv")
    var_v.append("1")
elif 'WIND' in system:
    var_n.append("F_pv")
    var_v.append("0")

suffix=results.results_file.split(".")[-1]

from solartherm import simulation
sim = simulation.Simulator(fn=fn, suffix=suffix, fusemount=False)
if not os.path.exists(model):
    sim.compile_model()
    sim.compile_sim(args=['-s'])

sim.update_pars(var_n, var_v)

try:
    sim.simulate(start='0', stop='1y', step='5m', initStep=None, maxStep='5m', integOrder='1e-06', solver='dassl', nls='homotopy', lv='-LOG_SUCCESS,-stdout')
    res_fn=sim.res_fn
    res=DyMat.DyMatFile(res_fn)

    if 'BAT' in system:
        LCOH=process_BAT(res, obj_cf=obj_cf)

    elif 'TES' in system:
        LCOH=process_TES(res, obj_cf=obj_cf)

    elif 'PHES' in system:
        LCOH=process_PHES(res, obj_cf=obj_cf)

    os.system('rm %s'%res_fn)
    os.system('rm %s_init_%s.xml'%(model,suffix))

except:
    LCOH=99999


res=[LCOH]


for i, r in enumerate(results.responses()):
	if r.asv.function:

		r.function = res[i]
results.write()

'''


    with open('interface_bb.py', 'w') as f:
        f.write(bb)  


def process_BAT(res, year=2020, obj_cf=None, verbose=False):
    pm=Parameters()
    CF=res.data('CF')[-1]
    RM=res.data('RM')[-1]
    t_storage=res.data('t_storage')[-1]
    F_pv=res.data('F_pv')[-1]
    pv_max=res.data('P_pv_des')[0]/1e3# kW
    wind_max=res.data('P_wind_des')[0]/1e3 # kW
    P_heater=res.data('P_heater')[0]/1e3 # kW
    bat_pmax=res.data('P_ST_max')[0]/1e3 # kW
    bat_capa=res.data('E_ST_max')[0]/1e3/3600. # kWh
    P_load_des=res.data('P_load')[0]/1e3 # kW
    eta_storage=res.data('eff_ST_in')[0]

    pm=Parameters()
    if year==2020:
        C_pv=pm.c_pv_system*pv_max
        C_wind=pm.c_wind_system*wind_max
        C_heater=P_heater*pm.c_heater
        C_bat=bat_capa*pm.c_bt_energy+bat_pmax*pm.c_bt_power

    elif year==2030:
        C_pv=pm.c_pv_system_2030*pv_max
        C_wind=pm.c_wind_system_2030*wind_max
        C_heater=P_heater*pm.c_heater_2030
        C_bat=bat_capa*pm.c_bt_energy_2030+bat_pmax*pm.c_bt_power_2030

    elif year==2050:
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

    LCOH, epy, OM_total=cal_LCOH(CF,  P_load_des, C_cap, OM_fixed, c_OM_var, r_discount=pm.r_disc_real, t_life=pm.t_life, t_cons=pm.t_constr_pv)

    print('RM=%.1f, SH=%.1f, F_pv=%.3f, P_bat=%.1f (MW), CF=%.4f, LCOH=%.2f'%(RM, t_storage,  F_pv, bat_pmax/1e3, CF, LCOH))	

    if verbose:
        summary=np.array([
                ['RM',RM, '-'],
                ['t_storage', t_storage, 'h'],
                ['LCOH', LCOH, 'USD/MWh_th'],
                ['CF', CF, '-'],
                ['F_pv', F_pv, '-'],
                ['pv_max', pv_max/1e3, 'MW'],
                ['wind_max', wind_max/1e3, 'MW'],
                ['P_heater',P_heater/1e3, 'MW'],
                ['bat_capa',bat_capa/1e3, 'MWh'],
                ['bat_pmax',bat_pmax/1e3, 'MW'],
                ['storage in/out efficiency', eta_storage, '-'],
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
                ['t_life', pm.t_life, 'year']            
        ])

        np.savetxt('./summary_%.3f_%.2f.csv'%(RM, t_storage), summary, fmt='%s', delimiter=',')


    if obj_cf!=None:
        if CF<obj_cf:
            LCOH=99999
    return LCOH


def process_PHES(res, year=2020, obj_cf=None, verbose=False):
    pm=Parameters()
    CF=res.data('CF')[-1]
    RM=res.data('RM')[-1]
    t_storage=res.data('t_storage')[-1]
    F_pv=res.data('F_pv')[-1]
    pv_max=res.data('P_pv_des')[0]/1e3# kW
    wind_max=res.data('P_wind_des')[0]/1e3 # kW
    P_heater=res.data('P_heater')[0]/1e3 # kW
    P_ST_max=res.data('P_ST_max')[0]/1e3 # kW
    E_ST_max=res.data('E_ST_max')[0]/1e3/3600. # kWh
    P_load_des=res.data('P_load')[0]/1e3 # kW
    eta_storage=res.data('eff_ST_in')[0]


    if year ==2020:
        C_pv=pm.c_pv_system*pv_max
        C_wind=pm.c_wind_system*wind_max
        C_heater=P_heater*pm.c_heater
        C_PHES=E_ST_max*pm.c_PHES_energy+P_ST_max*pm.c_PHES_power

    elif year==2030:
        C_pv=pm.c_pv_system_2030*pv_max
        C_wind=pm.c_wind_system_2030*wind_max
        C_heater=P_heater*pm.c_heater_2030
        C_PHES=E_ST_max*pm.c_PHES_energy_2030+P_ST_max*pm.c_PHES_power_2030


    elif year==2050:
        C_pv=pm.c_pv_system_2050*pv_max
        C_wind=pm.c_wind_system_2050*wind_max
        C_heater=P_heater*pm.c_heater_2050
        C_PHES=E_ST_max*pm.c_PHES_energy_2050+P_ST_max*pm.c_PHES_power_2050

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


    C_cap=CAPEX*(1+pm.r_conting_pv)+C_replc_heater_NPV

    OM_fixed=pm.c_om_pv_fix*pv_max+pm.c_om_wind_fix*wind_max+pm.c_om_PHES_fix*P_ST_max
    c_OM_var = pm.c_om_PHES_var

    LCOH, epy, OM_total=cal_LCOH(CF,  P_load_des, C_cap, OM_fixed, c_OM_var, r_discount=pm.r_disc_real, t_life=pm.t_life, t_cons=pm.t_constr_pv)

    print('RM=%.1f, SH=%.1f, F_pv=%.3f, P_ST_max=%.1f (MW), CF=%.4f, LCOH=%.2f'%(RM, t_storage,  F_pv, P_ST_max/1e3, CF, LCOH))	

    if verbose:
        summary=np.array([
                ['RM',RM, '-'],
                ['t_storage', t_storage, 'h'],
                ['LCOH', LCOH, 'USD/MWh_th'],
                ['CF', CF, '-'],
                ['F_pv', F_pv, '-'],
                ['pv_max', pv_max/1e3, 'MW'],
                ['wind_max', wind_max/1e3, 'MW'],
                ['P_heater',P_heater/1e3, 'MW'],
                ['PHES_capa',E_ST_max/1e3, 'MWh'],
                ['PHES_pmax',P_ST_max/1e3, 'MW'],
                ['storage in/out efficiency', eta_storage, '-'],
                ['EPY', epy, 'MWh'],
                ['C_cap_tot', C_cap/1e6, 'M.USD'],
                ['OM_tot', OM_total/1e6, 'M.USD'],
                ['C_equipment', CAPEX/1e6, 'M.USD'],
                ['C_pv', C_pv/1e6, 'M.USD'],            
                ['C_wind', C_wind/1e6, 'M.USD'],  
                ['C_PHES', C_PHES/1e6, 'M.USD'],  
                ['C_heater', C_heater/1e6, 'M.USD'],  
                ['C_replace_heater_NPV', C_replc_heater_NPV/1e6, 'M.USD'],   
                ['r_real_discount', pm.r_disc_real, '-'],
                ['t_construction', pm.t_constr_pv, 'year'],
                ['t_life', pm.t_life, 'year']              
        ])

        np.savetxt('./summary_%.3f_%.2f.csv'%(RM, t_storage), summary, fmt='%s', delimiter=',')


    if obj_cf!=None:
        if CF<obj_cf:
            LCOH=99999

    return LCOH

def process_TES(res, year=2020, obj_cf=None, verbose=False):
    pm=Parameters()
    CF=res.data('CF')[-1]
    RM=res.data('RM')[-1]
    t_storage=res.data('t_storage')[-1]
    F_pv=res.data('F_pv')[-1]
    pv_max=res.data('P_pv_des')[0]/1e3# kW
    wind_max=res.data('P_wind_des')[0]/1e3 # kW
    P_heater=res.data('P_heater_max')[0]/1e3 # kW
    TES_capa=res.data('E_ST_max')[0]/1e3/3600. # kWh
    P_load_des=res.data('P_load')[0]/1e3 # kW
    eta_storage=res.data('eff_ST_in')[0]

    pm=Parameters()
    if year ==2020:
        C_pv=pm.c_pv_system*pv_max
        C_wind=pm.c_wind_system*wind_max
        C_heater=P_heater*pm.c_heater
        C_TES=TES_capa*pm.c_TES

    elif year==2030:
        C_pv=pm.c_pv_system_2030*pv_max
        C_wind=pm.c_wind_system_2030*wind_max
        C_heater=P_heater*pm.c_heater_2030
        C_TES=TES_capa*pm.c_TES_2030

    elif year==2050:
        C_pv=pm.c_pv_system_2050*pv_max
        C_wind=pm.c_wind_system_2050*wind_max
        C_heater=P_heater*pm.c_heater_2050
        C_TES=TES_capa*pm.c_TES_2050

    else:
        print('Year %s data is not implemented'%year)


    CAPEX=C_pv+C_wind+C_heater+C_TES

   # heater replacement
    C_replace_heater=P_heater*pm.c_replace_heater
    n_replace_heater=int(pm.t_life/pm.t_life_heater)
    C_replc_heater_NPV=0
    for i in range(n_replace_heater):
        t=(i+1)*pm.t_life_heater+pm.t_constr_pv
        C_replc_heater_NPV+=C_replace_heater/(1+pm.r_disc_real)**t

    C_replace_NPV=C_replc_heater_NPV

    C_cap=CAPEX*(1+pm.r_conting_pv)+C_replace_NPV

    OM_fixed=pm.c_om_pv_fix*pv_max+pm.c_om_wind_fix*wind_max
    c_OM_var = 0.

    LCOH, epy, OM_total=cal_LCOH(CF,  P_load_des, C_cap, OM_fixed, c_OM_var, r_discount=pm.r_disc_real, t_life=pm.t_life, t_cons=pm.t_constr_pv)

    print('RM=%.1f, SH=%.1f, F_pv=%.3f, P_heater=%.1f (MW), CF=%.4f, LCOH=%.2f'%(RM, t_storage,  F_pv, P_heater/1e3, CF, LCOH))	
    
    if verbose:
        summary=np.array([
                ['RM',RM, '-'],
                ['t_storage', t_storage, 'h'],
                ['LCOH', LCOH, 'USD/MWh_th'],
                ['CF', CF, '-'],
                ['F_pv', F_pv, '-'],
                ['pv_max', pv_max/1e3, 'MW'],
                ['wind_max', wind_max/1e3, 'MW'],
                ['P_heater',P_heater/1e3, 'MW'],
                ['TES_capa',TES_capa/1e3, 'MWh'],
                ['storage in/out efficiency', eta_storage, '-'],
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
                ['t_life', pm.t_life, 'year']                 
        ])

        np.savetxt('./summary_%.3f_%.2f.csv'%(RM, t_storage), summary, fmt='%s', delimiter=',')


    if obj_cf!=None:
        if CF<obj_cf:
            LCOH=99999

    return LCOH



if __name__=='__main__':

    location='Burnie'
    mofn='/media/yewang/Data/Work/Research/Topics/yewang/HILTCRC/repo/RenewableTherm/PVWindEES.mo'

    method='Nelder-Mead'
    LB=[500e6, 0.]
    UB=[5000e6, 1.]
    nominals=[600e6, 0.9]
    names=['P_bat', 'r_pv']

    #objective_function(sim, 60, 9, par_n=['r_pv', 'P_bat'], par_v=[1., 1230.95200449223e6])
    #st_sciopt(sim, t_storage=20, RM=3.5, method=method, LB=LB, UB=UB, nominals=nominals, names=names, maxiter=100)

    RM=np.append(np.arange(1, 5, 0.5), np.arange(5, 11, 2))
    SH=np.r_[1e-6,2,4,6,8,10,12,14,17,20,25,40,60]
    #RM=np.r_[3.5]
    #SH=np.arange(12, 16, 2)
    for rm in RM:
        for sh in SH:
            res_fn='./summary_%.3f_%.2f.csv'%(rm, sh)
            if not os.path.exists(res_fn):
                st_sciopt(sim, t_storage=sh, RM=rm, method=method, LB=LB, UB=UB, nominals=nominals, names=names)
            else:
                print('RM', rm, 'SH', sh, 'Done')

