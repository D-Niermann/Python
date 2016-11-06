print "Starting..."
import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import matplotlib.image as img
import os,time,seaborn
from math import exp,sqrt,sin
print u"Finished importing"

seaborn.set_style("poster",
    {
    'axes.grid': False,
    'grid.linestyle': u'-',
    'legend.numpoints': 1,
    'legend.scatterpoints': 1,
    'axes.linewidth': 1.0,
    'xtick.direction': 'in',
    'ytick.direction': 'in',
    'legend.frameon': True,
    'ytick.minor.size': 4.0
    })


def function(x_min,x_max,y_min,y_max,c,d):
    plt.plot([x_min,x_max],[y_min,y_min],c,lw=1,label=d)
    plt.plot([x_min,x_max],[y_max,y_max],c,lw=1)
    plt.plot([x_max,x_max],[y_min,y_max],c,lw=1)
    plt.plot([x_min,x_min],[y_min,y_max],c,lw=1)
    # plt.plot([x_min,x_min],[0,y_min],"--",color=c,alpha=0.2)
    # plt.plot([x_max,x_max],[0,y_min],"--",color=c,alpha=0.2)

plt.figure("Scatter",figsize=(4,4))
plt.xlim([0,255])
plt.ylim([0,255])
plt.xlabel("Red Channel Intensity")
plt.ylabel("NIR Channel Intensity")
###############################
function(5,20,60,90,"g","High vegetation")
function(15,50,20,35,"r","Water")
function(20,30,90,170,"b","Low vegetation")
function(30,60,30,70,"y","Dense city")
function(25,45,40,70,"m","Sparse city")
function(60,255,70,255,"k","Clouds")
plt.legend()
plt.tight_layout()
plt.show()

#bla bla