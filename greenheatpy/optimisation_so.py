from scipy import optimize as sciopt
from greenheatpy.master import master
import functools

def objective_function(model_name, location, P_load_des, RM, SH, r_pv, P_heater, bat_pmax, casedir, verbose, par_n, par_v):

    nv=len(par_n)
    for i in range(nv):
        if par_n[i]=='RM':      
            RM=par_v[i]
        elif par_n[i]=='SH':
            SH=par_v[i]
        elif par_n[i]=='r_pv':
            r_pv=par_v[i]
        elif par_n[i]=='P_heater':
            P_heater=par_v[i]
        elif par_n[i]=='bat_pmax':
            bat_pmax=par_v[i]

    LCOH, CF, CAPEX=master(model_name, location, RM=RM, t_storage=SH, P_load_des=P_load_des, r_pv=r_pv, P_heater=P_heater, bat_pmax=bat_pmax, casedir=casedir, verbose=verbose)

    return LCOH 


def st_sciopt(model_name, location, P_load_des, RM, SH, r_pv, P_heater, bat_pmax, casedir, verbose, method, LB, UB, nominals, names,  maxiter=100):
    '''
    Arguments:
        model_name (str)  : minizic model name
        location   (str)  : site location
        P_load_des (float): system load design power (kW)
        RM         (float): renewable multiple, the total size of the renewable energy collection system (e.g. PV+Wind) to the load
        SH         (float): storage hour (h)
		r_pv       (float): fraction of pv, 1 is 100% pv, 0 is 100% wind, required by the pv+wind hybrid model
		P_heater   (float): electric power of the heater (kW), required by the pv/wind/hybrid+TES model
		bat_pmax   (float): power of the battery (kW), required by the pv/wind/hybrid+battery model
        casedir    (str)  : the case directory, if the default None is kept, it will load/save data in 'datadir'
        verbose    (bool) : to save and plot the time series results or not
   
        method     (str)  : the optimisation algorithm that is available in scipy package
                    e.g. 'Nelder-Mead', 'COBYLA', 'SLSQP', 'TNC', 
                        'L-BFGS-B' (can be used for maximisation)
        LB         (list) : lower bounds of all the variables
        UB         (list) : upper bounds of all the variables
        nominals   (list) : nominal values of all the variables
        names      (list) : names of all the variables
        maxiter    (int)  : max number of iterations
        
        
    '''
    bounds=[]
    nv=len(nominals)
    for i in range(nv):
        bounds.append([LB[i], UB[i]])        

    objfunc = functools.partial(objective_function, model_name, location, P_load_des, RM, SH, r_pv, P_heater, bat_pmax, casedir, verbose, names)


    res = sciopt.minimize(objfunc, nominals, method=method, bounds=bounds,
			options={
				'maxiter': maxiter,
				'disp': True,
			})

    print("")
    print('-----------')
    print('results',res)
    print('-----------')
    print("")
    #cand = [scale[i]*v + offset[i] for i, v in enumerate(res.x)]

    return res.fun, res.x


if __name__=='__main__':
    model_name='pv_wind_TES_heat'
    location='Newman'
    P_load_des=500e3
    RM=2
    SH=8
    r_pv=1.
    P_heater=None
    bat_pmax=None
    casedir='test-soo' 
    verbose=False
    method='Nelder-Mead'   
    LB=[500e3]
    UB=[3000e3]
    nominals=[505e3]
    names=['P_heater']
    fun, x=st_sciopt(model_name, location, P_load_des, RM, SH, r_pv, P_heater, bat_pmax, casedir, verbose, method, LB, UB, nominals, names,  maxiter=100)    
    print(fun)
    print('')
    print(x)
    print(type(fun), type(x))








