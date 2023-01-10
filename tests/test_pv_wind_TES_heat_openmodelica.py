import pandas as pd
import numpy as np
import os
from greenheatpy.optimisation_so_modelica import st_sciopt

import unittest
import matplotlib.pyplot as plt


class TestMasterHeat(unittest.TestCase):

	def setUp(self):
		location='Newman'
		RM=2
		t_storage=8
		LB=[500e6, 0.]
		UB=[5000e6, 1.]
		nominals=[600e6, 0.9]
		names=['P_heater', 'r_pv']
		mofn='../../RenewableTherm/PVWindTES.mo'
		self.casedir='test-TES-om'
		st_sciopt(mofn, location, t_storage=t_storage, RM=RM, method='Nelder-Mead', LB=LB, UB=UB, nominals=nominals, names=names,  casedir=self.casedir, case='TES')


	def test(self):

		results=np.loadtxt(self.casedir+'/summary_2.000_8.00.csv', delimiter=',', dtype=str)

		LCOH=results[2,1].astype(float)
		CF=results[3,1].astype(float)
		P_heater=results[7,1].astype(float)
		r_pv=results[4,1].astype(float)

		self.assertTrue(abs(LCOH-60.37)/60.37<0.05) 
		self.assertTrue(abs(CF-0.5677)/0.5677<0.05) 
		self.assertTrue(abs(P_heater-724.9)/724.9<0.05) 
		self.assertTrue(abs(r_pv-0.639)/0.639<0.05)    

		os.system('rm -r %s'%self.casedir)

        
if __name__=='__main__':
	unittest.main()
    








