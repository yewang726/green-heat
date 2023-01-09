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
		names=['P_ST_max', 'r_pv']
		mofn='../RenewableTherm/PVWindEES.mo'

		st_sciopt(mofn, location, t_storage=t_storage, RM=RM, method='Nelder-Mead', LB=LB, UB=UB, nominals=nominals, names=names, case='BAT')


	def test(self):

		results=np.loadtxt('./summary_2.000_8.00.csv', delimiter=',', dtype=str)

		LCOH=results[2,1].astype(float)
		CF=results[3,1].astype(float)
		P_ST=results[9,1].astype(float)
		r_pv=results[4,1].astype(float)

		self.assertTrue(abs(LCOH-138.81)/138.81<0.05) 
		self.assertTrue(abs(CF-0.4767)/0.4767<0.05) 
		self.assertTrue(abs(P_ST-500)/500<0.05) 
		self.assertTrue(abs(r_pv-1.)/1.<0.05)    

		os.system('rm PVWindEES*')
		os.system('rm summary*.csv')

        


if __name__=='__main__':
	unittest.main()
    








