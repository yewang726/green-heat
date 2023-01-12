import pandas as pd
import numpy as np
import os
from greenheatpy.optimisation_so_modelica import st_sciopt
from greenheatpy.projdirs import modelica_dir
from greenheatpy.get_green_h2 import get_best_location

import unittest
import matplotlib.pyplot as plt


class TestMasterHeat(unittest.TestCase):

    def setUp(self):
        best=get_best_location(2020)
        location='Pilbara'+' %s'%best['Pilbara']
        #location='Newman'
        solcast_TMY=False

        RM=2
        t_storage=8
        LB=[500e6, 0.]
        UB=[5000e6, 1.]
        nominals=[600e6, 0.9]
        names=['P_heater', 'r_pv']
        mofn=modelica_dir+'PVWindTES.mo'
        self.casedir='test-TES-om'
        st_sciopt(mofn, location, t_storage=t_storage, RM=RM, method='Nelder-Mead', LB=LB, UB=UB, nominals=nominals, names=names,  casedir=self.casedir, case='TES', solcast_TMY=solcast_TMY)


    def test(self):

        results=np.loadtxt(self.casedir+'/summary_2.000_8.00.csv', delimiter=',', dtype=str)

        LCOH=results[2,1].astype(float)
        CF=results[3,1].astype(float)
        P_heater=results[7,1].astype(float)
        r_pv=results[4,1].astype(float)

        self.assertTrue(abs(LCOH-41.35)/41.35<0.05) 
        self.assertTrue(abs(CF-0.8436)/0.8436<0.05) 
        self.assertTrue(abs(P_heater-662.2)/662.2<0.05) 
        self.assertTrue(abs(r_pv-0.532)/0.532<0.05)    

        os.system('rm -r %s'%self.casedir)

        
if __name__=='__main__':
	unittest.main()
    








