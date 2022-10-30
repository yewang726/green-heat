# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 10:32:04 2022

@author: Ahmad Mojiri and John Pye
"""

import os,platform
from pathlib import Path

#connector = ['\\','/'][platform.system()=='Linux']

basedir = Path(__file__).resolve().parents[2]
#if platform.system()=='Linux':
#    basedir = Path(__file__).resolve().parents[1]
#else:
#    # basedir = os.path.realpath('..') + connector
#    basedir = r'C:\\Nextcloud\\HILT-CRC---Green-Hydrogen\\'
    
datadir = basedir/'DATA'

# modeldir = basedir + "modelling%spython%spackage%s" %(connector, connector, connector)
optdir = basedir/'MINIZINC'# + "MINIZINC%s" %(connector)
# figdir = basedir + "modelling%sfigures%s" %(connector, connector)
# paperdir = basedir + "Publications%spaper_1%s" %(connector, connector)
# resultsdir = datadir + "arbitrage%s" %connector
