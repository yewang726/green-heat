import pandas as pd
import numpy as np
import os
from greenheatpy.projdirs import datadir #load the path that contains the data files 
from greenheatpy.optimisation_mo import gen_interface_bb, gen_dakota_input

import unittest
import matplotlib.pyplot as plt
import subprocess
import multiprocessing as mp

class TestMOO(unittest.TestCase):

    def setUp(self):
        location='Newman'
        model_name='pv_wind_TES_heat'
        self.casedir='test/test_moo'

        var_names=['RM', 't_storage', 'P_heater'] 
        nominals=[2, 8, 2000e3]
        lbs=[1, 1e-6, 500e3]
        ubs=[20, 60, 5000e3]

        if not os.path.exists(self.casedir):
            os.makedirs(self.casedir)

        os.chdir(self.casedir)

        # generate interface_bb.py that dakota can run
        gen_interface_bb(model_name, location, P_load_des=500e3)
        # generate dakota input file
        gen_dakota_input( var_names, nominals, lbs, ubs, num_eval=48)
        subprocess.call('chmod a+x interface_bb.py', shell=True)

        # run dakota
        np=mp.cpu_count()

        subprocess.call('mpirun --use-hwthread-cpus -np %s dakota -i sample.in -o sample.out > sample.stdout'%(4), shell=True)

    def test(self):

        res_fn='finaldata1.dat'

        self.assertTrue(os.path.exists(res_fn))
  
        #os.system('rm *.csv')

        


if __name__=='__main__':
    unittest.main()
    








