#-*- coding: utf-8 -*-
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
from scipy import integrate
import seaborn
seaborn.set(font_scale=1)

seaborn.set_style("ticks",
    {
    'axes.grid': True,
    'grid.linestyle': u'--',
    'axes.linewidth': 1.2,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'legend.frameon': True,
    })



def form1dlin(x,elm_id,node_id,grad=0):
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
		return Ni
	elif grad==1:
		if node_id==0:
			Ni=-1/(x2-x1)
		elif node_id==1:
			Ni=1/(x2-x1)
		return Ni

def form1dquad(x,elm_id,node_id,grad=0):
	#berechne wie viele elemente für quad:
	a=(len(xi)-1)/2.
	if a!=int(a): 
		print "Error 1"
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

def form_prod(x,elm_id,Node1,Node2,grad=0):
	return form1dlin(x,elm_id,Node1,grad)*form1dlin(x,elm_id,Node2,grad)
###########################################################################################


################ koordinaten der nodes, muss für quad 2*N+1 sein
# xi = [2.,4.,6.,8.]
xi   = np.linspace(0,8,21)
A    = 10		#Wärmeleitfähigkeit
k    = 5		#Wärmeleitung
Q    = 100.		#inhomogenität
q    = -15.
ga   = 100
################# Netz erstellen
ElmCon = []	#ereugt liste mit node id's. xi[ElmCon] gibt dann koordinaten
for  i in range(0,len(xi)-1):
	ElmCon.append([i,i+1])
print "ElmCon:",ElmCon



################ K Matrix erstellen
K=np.zeros([len(xi),len(xi)])
#gehe submatrizen durch ...jede matrix ist ein element zugehörig
for i in range(len(ElmCon)):	#gehe elemente durch
	for Node1 in range(len(ElmCon[i])):	#whäle rechte oder linke node
		for Node2 in range(len(ElmCon[i])):	#wähle andere node
			a=xi[ElmCon[i][0]]	#grenze für integral
			b=xi[ElmCon[i][1]]	#grenze für int
			K[ElmCon[i][Node1],ElmCon[i][Node2]]+=integrate.quad(form_prod,a,b,args=(i,Node1,Node2,1))[0]

K=A*k*K
print "K-Matrix:\n",K



############### f Vektor erstellen
f_L=np.zeros(len(xi))
for element in range(len(ElmCon)):
	for Node in range(len(ElmCon[element])):
		a=xi[ElmCon[element][0]]	#grenze für integral
		b=xi[ElmCon[element][1]]	#grenze für int
		f_L[ElmCon[element][Node]]+=Q*integrate.quad(form1dlin,a,b,args=(element,Node))[0]
print "Lastvektor:\n",f_L

f_Rand=np.zeros(len(xi))
f_Rand[-1]=q*A

f=f_L+f_Rand



############## Löse das Problem
"""aus der randbed dass T bei x=2 0 ist folgt dass man die erste zeile der K matrix 1,0,0,... 
setzen kann und den f vektor entssprechend 0 setzt. somit lässt sich die k matrix invertieren
und das problem lässt sich lösen"""
K[0,:]=0
K[0,0]=1
f[0]=ga
T=np.linalg.solve(K,f)
print "Temp: " , np.round(T,2)


#plotte alle formfunktionenen n(x)
x_max=xi[-1]

# for el_num in range(3):
# 	# plt.plot(np.arange(0,x_max,0.05),[form1dlin(x,el_num,2) for x in np.arange(0,x_max,0.05)],"r.-")
# 	plt.plot(np.arange(0,x_max,0.05),[form1dlin(x,el_num,1) for x in np.arange(0,x_max,0.05)],"g.-")
# 	plt.plot(np.arange(0,x_max,0.05),[form1dlin(x,el_num,0) for x in np.arange(0,x_max,0.05)],"b.-")
	
	# plt.plot(np.arange(0,x_max,0.05),[form1dlin(x,el_num,2,1) for x in np.arange(0,x_max,0.05)],"r--")
	# plt.plot(np.arange(0,x_max,0.05),[form1dlin(x,el_num,1,1) for x in np.arange(0,x_max,0.05)],"g--")
	# plt.plot(np.arange(0,x_max,0.05),[form1dlin(x,el_num,0,1) for x in np.arange(0,x_max,0.05)],"b--")
	
	# plt.plot(np.arange(0,x_max,0.1),[form_sum(x,i)     for x in np.arange(0,x_max,0.1)],".-")

# plotte T
plt.plot(xi,T)
plt.xlabel("x")
plt.ylabel("Temperatur "+r"$T$")
plt.show()

