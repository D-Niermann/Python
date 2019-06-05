""" 
Simple neural network, one of my first NN projects, only using numpy, requires MNIST dataset in readable form.
Teached me the basics of NNs

Created by Dario Niermann
2017
"""

# -*- coding: utf-8 -*-
if True:
	print( "Starting...")
	import numpy as np
	import numpy.random as rnd
	import matplotlib.pyplot as plt
	import matplotlib.image as img
	import scipy.ndimage.filters as filters
	import pandas as pd
	import os,time,seaborn
	from math import exp,sqrt,sin,pi,cos,log
	os.chdir(r"C:\Users\dniermann\Downloads\Projects")
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

	cwd=os.chdir("/Users/Niermann/Downloads/MNIST/training/")

	folders=os.listdir(os.getcwd())

log=Logger(True)

def vectorize(data):
	length=data.shape[0]*data.shape[1]
	data=data.reshape(length)
	return data

def heavyside(x):
	return int(x+0.5)

def sign(x):
	return 1./(1+np.exp(-x))

def Neuron(w,x,b):
	return sign(np.dot(w,x)-b)

def cost(output,target):
	return np.sum(np.abs(target-output)**2)

def feed_forward(AB):
	# matrix for all neurons activations
	activations=[]
	for j in range(len(num_neurons)):
		activations.append(np.zeros((num_neurons[j])))
	
	#go through all layers
	for layer in range(len(num_neurons)):
		# for neuron in range(num_neurons[layer]):
		if layer==0:
			a=AB
			activations[layer]=a
		else:		
			a=sign(np.dot(Weights[layer-1],activations[layer-1])-bias[layer])
			activations[layer]=a
	return activations

def cross_entropy(output,target):
	output=np.array(output)
	target=np.array(target)
	return -np.sum(target*np.log(output)+(1-target)*np.log(1-output))
	
def get_y(num_neurons):
	ys=[]
	max_n=float(max(num_neurons))
	for i,n in enumerate(num_neurons):
		if n!=1:
			lin=np.linspace(-n/max_n,n/max_n,n)
			ys.append([np.ones(len(lin))*i,lin])
		elif n==1:
			lin=np.linspace(-n/max_n,n/max_n,n)
			ys.append([np.ones(len(lin))*i,[0]])
	return ys

def make_diag(matrix):
	if matrix.shape[0]==matrix.shape[1]:
		return np.diag(np.diag(matrix))
	else:
		return matrix

def mutate(Weights,fully_connected=True):
	Delta_W=[]

	for k in range(1,len(num_neurons)):
		shape=[num_neurons[k],num_neurons[k-1]]

		if shape[0]==shape[1] and fully_connected==False:
			Delta_W.append(
				make_diag(
					(rnd.random(shape)-0.5)*learnrate
				)
			)
		else:
			Delta_W.append(
				(rnd.random(shape)-0.5)*learnrate
			)

	Weights+=Delta_W
	return Weights,Delta_W

######################## Variables ###########################################


## Number of neurons in the i'th layer
num_neurons = [10,30,3]
learnrate   = 0.03
steps       = 400

#### Anfangsbedingung ##############################################
#### get a random gaussian elipse
# N         = 1000
# data      = rnd.randn(N,N)
# data[0]   = data[0]*4
# data2     = rnd.randn(N,N)+10
# data2[0]  = data2[0]*2
# data_zip  = zip(data[0],data[1])
# data2_zip = zip(data2[0],data2[1])
# data_AB   = data_zip+data2_zip
#################################################
AB  = [rnd.random(10)]
Soll = [1,0,0]
#################################################


# for f in folders:
# 	os.chdir("/Users/Niermann/Downloads/MNIST/training/")
# 	if f[0]!=".":
# 		new_path="/Users/Niermann/Downloads/MNIST/training/"+f
# 		os.chdir(new_path)
# 		for i in os.listdir(os.getcwd()) [0:10]:
# 			images.append(
# 				vectorize(img.imread(i))
# 			)
# 			Soll_append=[0]*10
# 			Soll_append[int(f)]=1
# 			Soll.append(Soll_append)

# AB=images



######################## init ################################################

#init the weights for all layers in one 3D matrix called Weights
# Weights[i] is the connection between layers i and i+1
Weights=[]
for i in range(1,len(num_neurons)):
	Weights.append(
		(np.zeros([num_neurons[i],num_neurons[i-1]]))
		)

Weights=np.array(Weights)
# # Weights for XOR perzeptron:
# Weights[1][0,1]=-2
# Weights[0][0,1]=0
# Weights[0][2,0]=0


# bias for every neuron
bias=[]
for i in range(len(num_neurons)):
	bias.append(5*np.zeros((num_neurons[i])))
bias=np.array(bias)
# Set bias for XOR Perceptron
# bias[1][1]=2




############### iterate through every neuron and AB: ########################################
log.start("Mainloop")

cost_means=[0]


for ii in range(steps):
############ matrix for all neurons activations #############################################
	activations=[]
	for j in range(len(num_neurons)):
		activations.append(np.zeros((num_neurons[j])))

############ Mutation ########################################################################
	if ii==0:
		Weights,Delta_W=mutate(Weights,fully_connected=True)
	else:
		if cost_means[ii-1]>cost_means[ii]:
			Weights+=Delta_W
		else:
			Weights,Delta_W=mutate(Weights,fully_connected=True)

########### Feed Forward for all training inputs in AB ######################################
	costs=[]
	results=[]
	for i,AB_ in enumerate(AB):
		activations=feed_forward(AB_)
		results.append(activations[-1])
		costs.append(cross_entropy(results[i],Soll[i]))

	cost_means.append(np.mean(costs))

	if ii%50==0:
		log.out("Mean Cost:",np.mean(costs))
		log.info("Completed",ii/float(steps)*100,"%")
################################################################################################

######################## Plot ###########################################
plt.plot(cost_means)
# plt.figure()
# plt.imshow(np.diag(Weights[0]).reshape(28,28),interpolation="nearest")
# plt.colorbar()
ys=get_y(num_neurons)
plt.show()

if True:
	plt.figure()
	log.start("Plot")
	W_max=-1e10
	for i in range(len(Weights)):
		if np.max(Weights[i])>W_max:
			W_max=np.max(Weights[i])

	for layer in range(len(ys)-1):
		for neuron in range(0,len(ys[layer][0])):
			for neuron2 in range(0,len(ys[layer+1][0])):
				x1=ys[layer][0][neuron]
				y1=ys[layer][1][neuron]
				x2=ys[layer+1][0][neuron2]
				y2=ys[layer+1][1][neuron2]
				try:
					lw=Weights[layer][neuron2,neuron]/W_max
					if abs(lw)>0.01:
						if lw>0:
							plt.plot([x1,x2],[y1,y2],"g",lw=abs(lw)**2)
						else:
							plt.plot([x1,x2],[y1,y2],"r",lw=abs(lw)**2)
				except:
					print( "error plotting")
	for i in ys:
		plt.plot(i[0],i[1],"o",markersize=10)
	plt.xlim(-0.1,len(num_neurons)-1+0.1)
	plt.ylim(-1.1,1.1)
	log.end()
	plt.show()
	log.end()
	# plt.plot(range(-100,100),[Neuron(1,i,10) for i in range(-100,100)])
	# plt.show()