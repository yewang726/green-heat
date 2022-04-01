# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 10:32:04 2022

@author: Ahmad Mojiri
"""

import sys, os
 
connector = '\\'
basedir = os.path.realpath('..') + connector
    

datadir = basedir + "DATA%s" %connector
# modeldir = basedir + "modelling%spython%spackage%s" %(connector, connector, connector)
optdir = basedir + "minizinc%s" %(connector)
# figdir = basedir + "modelling%sfigures%s" %(connector, connector)
# paperdir = basedir + "Publications%spaper_1%s" %(connector, connector)
# resultsdir = datadir + "arbitrage%s" %connector