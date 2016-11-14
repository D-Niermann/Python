import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
from scipy import integrate
import seaborn
seaborn.set_style("ticks",
    {
    'axes.grid': True,
    'grid.linestyle': u'--',
    'axes.linewidth': 1.2,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'legend.frameon': True,
    })



def form1dlin(x,elm_id,node_id,grad):
	"""Erzeugt formfunktion: linierae anpassung zwischen 2 Nodes welche nebeneinander 
	sind. Überall anders =0. Node ID =0 heisst das die linke node des elements 
	genommen wird und =1 heisst rechte node"""
	x1=xi[ElmCon[elm_id][0]]
	x2=xi[ElmCon[elm_id][1]]
	h=0.001
	#gucke ob x überhaupt im Eleemnt liegt
	if x>xi[ElmCon[elm_id][1]] or x<xi[ElmCon[elm_id][0]]: #liegt ausserhalb vom element
		Ni=0
		return Ni

	if grad==0:
		if node_id==0:
			Ni=(x2-x)/(x2-x1)
		elif node_id==1:
			Ni=(x-x1)/(x2-x1)
	elif grad==1:
		if node_id==0:
			Ni=-1/(x2-x1)
		elif node_id==1:
			Ni=1/(x2-x1)
	return Ni

def form1dquad(x,elm_id,node_id,grad):
	#berechne wie viele elemente für quad:
	a=(len(xi)-1)/2.
	if a!=int(a): 
		return None

	x1 = xi[ElmCon[elm_id][0]]
	x2 = xi[ElmCon[elm_id][1]]
	x3 = xi[ElmCon[elm_id][2]]
	h=0.01

	if x>xi[ElmCon[elm_id][2]] or x<xi[ElmCon[elm_id][0]]:
		Ni=0
		return Ni

	if grad==0:	
		if node_id==0:
			Ni=1/((x1-x2)*(x1-x3))*(x-x2)*(x-x3)
		if node_id==1:
			Ni=1/((x2-x1)*(x2-x3))*(x-x1)*(x-x3)
		if node_id==2:
			Ni=1/((x3-x1)*(x3-x2))*(x-x1)*(x-x2)
		return Ni
	elif grad==1:
		if node_id==0:
			Ni=(1/((x1-x2)*(x1-x3))*(x+h-x2)*(x+h-x3)-1/((x1-x2)*(x1-x3))*(x-x2)*(x-x3))/h
		if node_id==1:
			Ni=(1/((x2-x1)*(x2-x3))*(x+h-x1)*(x+h-x3)-1/((x2-x1)*(x2-x3))*(x-x1)*(x-x3))/h
		if node_id==2:
			Ni=(1/((x3-x1)*(x3-x2))*(x+h-x1)*(x+h-x2)-1/((x3-x1)*(x3-x2))*(x-x1)*(x-x2))/h
		return Ni

def form_sumquad(x,elm_id):
	return form1dquad(x,elm_id,0)+form1dquad(x,elm_id,1)+form1dquad(x,elm_id,2)

###########################################################################################


xi = [0.,1.,2.,5.,1,6.] #koordinaten der nodes, muss für quad 2*N+1 sein
# xi=np.linspace(0,10,21)



ElmCon = []	#ereugt liste mit node id's. xi[ElmCon] gibt dann koordinaten
for  i in range(0,len(xi)-2,2):
	ElmCon.append([i,i+1,i+2])
print ElmCon


#plotte alle formfunktionenen n(x)
x_max=5
for el_num in range(1):
	plt.plot(np.arange(0,x_max,0.01),[form1dquad(x,el_num,2,0) for x in np.arange(0,x_max,0.01)],"r.-")
	plt.plot(np.arange(0,x_max,0.01),[form1dquad(x,el_num,1,0) for x in np.arange(0,x_max,0.01)],"g.-")
	plt.plot(np.arange(0,x_max,0.01),[form1dquad(x,el_num,0,0) for x in np.arange(0,x_max,0.01)],"b.-")
	plt.plot(np.arange(0,x_max,0.01),[form1dquad(x,el_num,2,1) for x in np.arange(0,x_max,0.01)],"r--")
	plt.plot(np.arange(0,x_max,0.01),[form1dquad(x,el_num,1,1) for x in np.arange(0,x_max,0.01)],"g--")
	plt.plot(np.arange(0,x_max,0.01),[form1dquad(x,el_num,0,1) for x in np.arange(0,x_max,0.01)],"b--")
	# plt.plot(np.arange(0,x_max,0.1),[form_sum(x,i)     for x in np.arange(0,x_max,0.1)],".-")
plt.show()

