import pandas as pd
import numpy as np
import os
from projdirs import datadir #load the path that contains the data files 
from master_heat import master

import unittest
import matplotlib.pyplot as plt


class TestMasterHeat(unittest.TestCase):

    def setUp(self):
        location='Newman'
        RM=2
        t_storage=8

        model_name='CST_TES_heat'
        self.casedir='test/'+model_name
        self.LCOH, CF=master(model_name, location, RM=RM, t_storage=t_storage, P_load_des=500e3, casedir=self.casedir, verbose=True)

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
        self.assertTrue(abs(self.LCOH-43.3)<1e-2)

        #os.system('rm *.csv')

        


if __name__=='__main__':
    unittest.main()
    








