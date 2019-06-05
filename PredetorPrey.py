# -*- coding: utf-8 -*-

"""
Very simple solver for a coupled differential equation. (predetor prey model)

Created by: Dario Niermann
Created around 2017
"""
from __future__ import unicode_literals
print( "Starting...")
import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import matplotlib.image as img
import scipy.ndimage.filters as filters
import pandas as pd
import os,time,seaborn
from math import exp,sqrt,sin,pi,cos,log
np.set_printoptions(precision=3)
from Logger import *
print( u"Finished importing")
# plt.style.use('ggplot')
seaborn.set(font_scale=1.4)
seaborn.set_style("ticks",
	{
	'axes.grid':            True,
	'grid.linestyle':       u':',
	'legend.numpoints':     1,
	'legend.scatterpoints': 1,
	'axes.linewidth':       1,
	'xtick.direction':      'in',
	'ytick.direction':      'in',
	'xtick.major.size': 	5,
 	'xtick.minor.size': 	1.0,
	'legend.frameon':       True,
	'ytick.major.size': 	5,
 	'ytick.minor.size': 	1.0
	})

# xp = a*x-b*x*y
# yp = -c*y + d*x*y

time = 10000
dt=0.1
a = 0.07
b = 0.05
c = 0.1
d = 0.08

x = np.zeros(time)
y = np.zeros(time)

x[0] = 1
y[0] = 1

for t in range(time-1):

	x[t+1] = x[t]+(x[t]*(a-b*y[t]))*dt
	y[t+1] = y[t]+(y[t]*(-c+d*x[t]))*dt


plt.plot(x,label="Beute")
plt.plot(y,label="Rauber")
plt.legend()
plt.figure()
plt.plot(x,y)
plt.show()