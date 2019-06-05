""" solving the heat equation

Created by Dario Niermann
2015
"""

 #!/usr/bin/env python
print( "Starting...")
import scipy as sp
import numpy as np
import seaborn
import matplotlib.pyplot  as plt
from matplotlib import animation
from pylab import *
seaborn.set(font_scale=1.4)

# Declare some variables:

dx=0.01        # Interval size in x-direction.
dy=0.01        # Interval size in y-direction.
a=0.5          # Diffusion constant.
timesteps=2000  # Number of time-steps to evolve system.

nx = int(1/dx)
ny = int(1/dy)

dx2=dx**2 # To save CPU cycles, we'll compute Delta x^2
dy2=dy**2 # and Delta y^2 only once and store them.

# For stability, this is the largest interval possible
# for the size of the time-step:
dt = (dx2*dy2/(2*a*(dx2+dy2)))

# Start u and ui off as zero matrices:
ui = sp.zeros([nx,ny])
u = sp.zeros([nx,ny])

# Now, set the initial conditions (ui).
for i in range(nx):
	for j in range(ny):
		if ( ( (i*dx-0.5)**2+(j*dy-0.5)**2 <= 0.1)
			& ((i*dx-0.5)**2+(j*dy-0.5)**2>=.05) ):
				ui[i,j] = 1

#inhomogenitat
u_in=np.zeros([98,98])
u_in2=np.zeros([98,98])
u_in[10:30,10:90]=400
u_in2[30:40,10:90]=400


def evolve_ts(u, ui,t):
	"""	inhomogener fall also du/dt-aΔu=u_in
	wird zu:	(u(t_2)-u(t_1))=dt*(u_in+aΔu) und u(t_2)=u(t_1)+dt*(u_in+aΔu)
	mit t_2>t_1

	u[1:-1, 1:-1] = ui[1:-1, 1:-1] #startpoint
	+ a*dt*(			#weil du/dt=du/dx2+du/dy2 ist und umgestellt wurde	
	(ui[2:, 1:-1] 		#2te abl in x: f(x+dx)
	- 2*ui[1:-1, 1:-1] 	#-2f(x)
	+ ui[:-2, 1:-1])/dx2 	#f(x-dx)
	
	+ (ui[1:-1, 2:] 		#2te abl in y
	- 2*ui[1:-1, 1:-1] 
	+ ui[1:-1, :-2])/dy2 
		)"""
	if t<30:
		u[1:-1, 1:-1] = u_in*dt+ ui[1:-1, 1:-1] + a*dt*( (ui[2:, 1:-1] - 2*ui[1:-1, 1:-1] + ui[:-2, 1:-1])/dx2 + (ui[1:-1, 2:] - 2*ui[1:-1, 1:-1] + ui[1:-1, :-2])/dy2 )
	elif t>30 and t<60:
		u[1:-1, 1:-1] = u_in2*dt+ ui[1:-1, 1:-1] + a*dt*( (ui[2:, 1:-1] - 2*ui[1:-1, 1:-1] + ui[:-2, 1:-1])/dx2 + (ui[1:-1, 2:] - 2*ui[1:-1, 1:-1] + ui[1:-1, :-2])/dy2 )		
	else:
		u[1:-1, 1:-1] = ui[1:-1, 1:-1] + a*dt*( (ui[2:, 1:-1] - 2*ui[1:-1, 1:-1] + ui[:-2, 1:-1])/dx2 + (ui[1:-1, 2:] - 2*ui[1:-1, 1:-1] + ui[1:-1, :-2])/dy2 )
	#boundry condition
	u[-1:]=0.5
	return u




#saves all iterations of u
master=np.zeros([timesteps,100,100])


#main calculation
for m in range(timesteps):
   	master[m]=ui
   	u=evolve_ts(u, ui,m)
   	ui=u


fig = plt.figure(figsize=(10,8))
ax=fig.add_subplot(111)

im = ax.imshow(master[0], animated=True,cmap="hot",vmin=0,vmax=1)
plt.colorbar(im)


i=0
def updatefig(i):
	ax.cla()
	plt.grid()
	ax.imshow(master[2*i],animated=True,cmap="hot",vmin=0,vmax=1,interpolation="bicubic")
	i+=1

ani = animation.FuncAnimation(fig, updatefig, interval=20,frames=timesteps-1,
	repeat=False, blit=False)
plt.show()