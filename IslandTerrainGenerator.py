"""
Generate height maps and plant spots randomly, also generating gravity based rivers.

Created by Dario Niermann
2015
"""
#-*- coding: utf-8 -*-
print( "Starting...")
import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.image as img
import scipy.ndimage.filters as filters
import os,time

from math import exp,sqrt,sin,pi,cos
print( u"Finished importing")


world_size=400
world=np.zeros([world_size,world_size])

odds=400

xs=[]
ys=[]
xs2=[]
ys2=[]
xs3=[]
ys3=[]

def height(i,j):
	i=float(i)
	j=float(j)
	x=(i-world_size/2)/(world_size/4)
	y=(j-world_size/2)/(world_size/4)
	return exp(-(x**2+y**2))

#Generate
for i in range(world_size):
	for j in range(world_size):
		if rnd.randint(odds)==0:
			world[i,j]=height(i, j)


#Blur
kernel_size=8
kernel_smooth = np.ones([kernel_size,kernel_size])*1/kernel_size**2
for i in range(30):
	world=filters.convolve(world,kernel_smooth)

#Normalize
world[:,:]=world[:,:]*1/np.max(world)

#Spawn Life
for i in range(world_size):
	for j in range(world_size):
		if world[i,j]>0.3 and world[i,j]<0.5:
			if rnd.randint(1000)==0:
				xs.append(i)
				ys.append(j)
		if world[i,j]>0.2 and world[i,j]<0.3:
			if rnd.randint(10)==0:
				xs2.append(i)
				ys2.append(j)
		if world[i,j]>0.45 and world[i,j]<0.65:
			if rnd.randint(100)==0:
				xs3.append(i)
				ys3.append(j)

#grow life
for k in range(300):
	i=rnd.randint(len(xs))
	a=xs[i]+rnd.randint(-5,6)
	b=ys[i]+rnd.randint(-5,6)
	if world[a,b]<0.6 and world[a,b]>0.2:
		# if a not in xs or b not in ys:
			xs.append(a) 
			ys.append(b)
	i=rnd.randint(len(xs3))
	a=xs3[i]+rnd.randint(-5,6)
	b=ys3[i]+rnd.randint(-5,6)
	if world[a,b]<0.75 and world[a,b]>0.25:
		# if a not in xs or b not in ys:
			xs3.append(a) 
			ys3.append(b)
#rivers
river=np.ones([world_size,world_size])

for k in range(10):
	start=np.where(world>0.9)
	c=rnd.randint(len(start[0])-1)
	start_x=start[0][c]
	start_y=start[1][c]
	a=start_x
	b=start_y
	a0=a
	b0=b

	for i in range(1000):
		pos=world[a0,b0]
		a=a0+rnd.randint(-1,2)
		b=b0+rnd.randint(-1,2)	
		if (a!=a0 and b!=b0): 
			if pos>world[a,b]:
				a0=a
				b0=b
				river[a:a+1,b:b+1]=0.3
#Blur
kernel_size=3
kernel_smooth = np.ones([kernel_size,kernel_size])*1/kernel_size**2
for i in range(3):
	river=filters.convolve(river,kernel_smooth)

world*=river

plt.figure("Map",figsize=(9,9))

plt.imshow(np.transpose(world),interpolation="nearest",cmap="terrain")

plt.scatter(xs,ys,color="g",alpha=0.2)
plt.scatter(xs2,ys2,color="y",alpha=0.2)
plt.scatter(xs3,ys3,color="#005500",alpha=0.2)
# plt.plot(world[200,:])

plt.show()
plt.close()