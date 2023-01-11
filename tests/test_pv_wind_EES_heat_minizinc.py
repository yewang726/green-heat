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

        model_name='pv_wind_battery_heat'
        self.casedir='test-EES-mnz'
        self.LCOH, self.CF, self.C_cap =master(model_name, location, RM=RM, t_storage=t_storage, P_load_des=500e3, r_pv=0.6, P_heater=500e3/0.99, bat_pmax=650e3, casedir=self.casedir, verbose=True, solcast_TMY=solcast_TMY)

    def test(self):

        pv_out=np.loadtxt(self.casedir+'/pv_out.csv', delimiter=',')
        wind_out=np.loadtxt(self.casedir+'/wind_out.csv',delimiter=',')
        P_ele=np.loadtxt(self.casedir+'/P_ele.csv',delimiter=',')
        P_curt=np.loadtxt(self.casedir+'/P_curt.csv', delimiter=',')
        P_bat_in=np.loadtxt(self.casedir+'/P_bat_in.csv', delimiter=',')
        P_bat_out=np.loadtxt(self.casedir+'/P_bat_out.csv', delimiter=',')

        # check
        pv_wind_direct=P_ele-P_bat_out
        check=sum(pv_out+ wind_out - P_curt - pv_wind_direct - P_bat_in)
        print('check=', check)
        self.assertTrue(check<1e-2)
        self.assertTrue(abs(self.LCOH-123.16)/123.16<0.05)
        self.assertTrue(abs(self.CF-0.573)/0.573<0.05)
        self.assertTrue(abs(self.C_cap-3401863691.6)/3401863691.6<0.05)
        os.system('rm -r '+self.casedir)

        


if __name__=='__main__':
    unittest.main()
    








