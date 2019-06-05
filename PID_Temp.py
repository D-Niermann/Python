"""
goal was to programm a simple PID to controll temperature in another real application project.
I simulated an very delayed heating, like it was observed in the real application and tried to mimic a PID
to better control the (binary on/off) heating. The goal is to heat a chamber from 22 to 24 degree celcius.
Without PID (set PARAM1 to 1) the heating overshoots, with good value of PARAM1 = 10 the PID does not overshoot and keeps T more constant around 4.

Created by Dario Niermann
2018
"""


PARAM1 = 10

print( "Starting...")
# import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import os,time,seaborn
print( "Finished importing")
heating=0
flux=0
temp=22
f,f2,f3=[],[],[]
keep=0
switch=0
for i in range(600):
	f.append(temp)
	temp+=flux-(0.01*(temp-22))-0.01*rnd.randint(-1,2) ##Temperaturdefinition
	if heating==1 and flux<0.2:
		flux+=0.001 ##dadurch Selbstverstaerkung
	elif heating==0 and flux>0:
		flux-=0.001 
	################################
	#berechne tangente -- eigentlicher PID Teil
	try:
		steigung=(f[-1]-f[-PARAM1])/PARAM1
		# f2.append(steigung)
	except:
		steigung=0
	#extrapoliere
	t_ex=0
	t=0
	if steigung >0.01:
		while t_ex<=24:
			t_ex=temp+t*steigung
			t+=1
	f2.append(t)


	if t>20 or t==0 and temp<24:
		heating=1
	else:
		heating=0
fig=plt.figure()
ax1=fig.add_subplot(211)
ax2=fig.add_subplot(212)
ax1.set_ylabel("Temp")
ax2.set_ylabel("Heating Demand")
ax1.plot(f)
ax2.plot(f2)
plt.show()

print( "Done!")
