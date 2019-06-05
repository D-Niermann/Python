"""
code for my physics class concerning the feigenbaum constant.

Created by Dario Niermann
2018
"""

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
print("Starting...")
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
print(u"Finished importing")
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


for x_0 in np.linspace(0,1,100):
	timesteps=200
	eps=0.001
	a=2.1
	x=np.zeros(timesteps)
	x[0]=x_0

	for t in range(timesteps-1):
		x[t+1]=a*x[t]*(1-x[t])

	# x=rnd.random(timesteps)
	sorted_x=sorted(x)
	diff=np.diff(sorted_x)

	num_of_peaks=0
	switch=0
	for i in range(1,len(diff)):
		if diff[i-1]>diff[i]+eps and switch==0:
			num_of_peaks+=1
			switch=1
		if diff[i-1]<eps:
			switch=0

	plt.scatter(x[0],x[3])


timesteps=200
eps=0.001
a=3.9
x=np.zeros(timesteps)
x[0]=0.0001

for t in range(timesteps-1):
	x[t+1]=a*x[t]*(1-x[t])

# x=rnd.random(timesteps)
sorted_x=sorted(x)
diff=np.diff(sorted_x)

num_of_peaks=0
switch=0
for i in range(1,len(diff)):
	if diff[i-1]>diff[i]+eps and switch==0:
		num_of_peaks+=1
		switch=1
	if diff[i-1]<eps:
		switch=0

plt.figure()
plt.plot(x)
# plt.figure()
# plt.plot(diff)



plt.show()