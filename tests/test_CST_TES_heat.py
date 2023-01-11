import pandas as pd
import numpy as np
import os
from greenheatpy.projdirs import datadir #load the path that contains the data files 
from greenheatpy.master import master

import unittest
import matplotlib.pyplot as plt


class TestMasterHeat(unittest.TestCase):

    def setUp(self):
        location='Newman' #'Pilbara 1'
        solcast_TMY=True
        RM=2
        t_storage=8

        model_name='CST_TES_heat'
        self.casedir='test-'+model_name
        self.LCOH, self.CF, self.C_cap=master(model_name, location, RM=RM, t_storage=t_storage, P_load_des=500e3, casedir=self.casedir, verbose=True, solcast_TMY=solcast_TMY)

    def test(self):

        P_recv_out=np.loadtxt(self.casedir+'/P_recv_out.csv', delimiter=',')
        P_curt=np.loadtxt(self.casedir+'/P_curt.csv', delimiter=',')
        P_direct=np.loadtxt(self.casedir+'/P_direct.csv', delimiter=',')
        P_TES_in=np.loadtxt(self.casedir+'/P_TES_in.csv', delimiter=',')
        P_TES_out=np.loadtxt(self.casedir+'/P_TES_out.csv', delimiter=',')
        P_heat=np.loadtxt(self.casedir+'/P_heat.csv', delimiter=',')

        # check

        balance_1 = sum(P_recv_out-P_direct-P_TES_in-P_curt)
        balance_2 = sum(P_TES_out + P_direct - P_heat)

        print('balance 1', balance_1)
        print('balance 2', balance_2)

        self.assertTrue(balance_1<1e-2)
        self.assertTrue(balance_2<1e-2)
        self.assertTrue(abs(self.LCOH-47.97)/47.91<0.05)
        self.assertTrue(abs(self.CF-0.525)/0.525<0.05)
        self.assertTrue(abs(self.C_cap-719978158.5)/719978158.5<0.05)

        os.system('rm -r %s'%self.casedir)

        


if __name__=='__main__':
    unittest.main()
    








