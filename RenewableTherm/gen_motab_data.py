import numpy as np
import matplotlib.pyplot as plt
import os
def gen_ref_power(data, name, savefile, plot=False):

    f=open(savefile, 'w')
    f.write('#1\n') 
    f.write('#METALABELS, time, %s\n'%name)
    f.write('double %s(8760,2)\n'%name)  
    for i in range(8760):
        f.write('%s, %s\n'%(3600*i, data[i]))
    f.close()    
    if plot:
        plt.plot(np.arange(8760), data)
        plt.show()
        plt.close()

if __name__=='__main__':
    if not os.path.exists('./data-motab'):
        os.makedirs('./data-motab')
    locations=['Newman', 'Burnie', 'Gladstone', 'Pinjarra', 'Port Augusta', 'Tom Price', 'Whyalla']
    for location in locations:
        data=np.loadtxt('./data/pv_gen_%s_1.0MWe.dat'%location, delimiter=',')
        gen_ref_power(data, name='PV_out_ref', savefile='./data-motab/PV_out_ref_%s.motab'%location)    
        data=np.loadtxt('./data/wind_gen_%s_200.0MWe.dat'%location, delimiter=',')
        gen_ref_power(data, name='Wind_out_ref', savefile='./data-motab/Wind_out_ref_%s.motab'%location)         
