# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 10:32:04 2022 by Ahmad Mojiri

Modified by Ye Wang to work with greenheatpy
"""

import os
import platform

## TODO
# setup basedir
basedir = '/media/yewang/Data/Work/Research/Topics/yewang/HILTCRC/repo' 

hilt_svn_repo='/media/yewang/Data/Work/Research/Topics/svn-hilt'
wea_repo= hilt_svn_repo+'/weather/TMY DATA for H2 HUBS/'

if platform.system()=="Windows":
	connector = '\\'
elif platform.system()=="Linux":
 	connector='/'

datadir = basedir + connector+ "data" + connector
minizinc_dir = basedir + connector + "greenheatpy"+ connector + "minizinc" + connector
modelica_dir = basedir + connector + "greenheatpy"+ connector + "modelica" + connector

