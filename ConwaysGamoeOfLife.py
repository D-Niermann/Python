"""
Conways Game of life Simulator tool with some analytics

Created by: Dario Niermann
"""

print( "**Starting...**")
import numpy as np
import numpy.random as rnd
import matplotlib.pyplot as plt
import matplotlib.image as img
import os,time,seaborn
from math import exp,sqrt
print( u"**Finished importing**")


def f(a):
	"""this function will count the neighbours of a pixel (cell) wich is
	in the middle of given 3x3 array a. Then it will decide whether
	the cell will survive or die."""

	if len(a)>2 and np.sum(a)>0:
		
		middle     = a[1,1]
		neighbours = np.sum(a)-middle
		n          = neighbours
		
		if middle == 1:			#cell alive
			if n>3 or n<2:
				return 0		#make dead
			else:
				return 1		#stay alvive
		else:					#dead cell
			if n == 3:
				return 1		#create cell
			else:
				return 0		#stay dead

	else:
		return 0



# plt.figure(figsize = (13,10))


n=0

xm       = 100		#maximum x lenght
ym       = 100		#maximum y length
max_gens = 300		#max generations
master   = np.zeros([max_gens,xm,ym])

while n<300:
	n+=1
	if n%20==0:
		print( "*",n," tries*")
	
	# ask=raw_input("next?")
	# if ask=="n":
	# 	break

	#making grid and placing cells
	grid            = np.zeros([xm,ym])
	number_of_cells = np.zeros([max_gens])
	
	#make random part grid
	random_area=slice(20,25)
	random_area2=slice(25,30)
	while np.sum(grid[random_area,random_area])==0:
		grid[random_area,random_area] = abs(np.round(np.add(rnd.random([5,5]),0.1)))
	grid[random_area2,random_area2]=np.fliplr(grid[random_area,random_area])
	

	start = grid[20:30,20:30]

	# print( "Starting with %s cells:"%str(np.sum(start)))
	# print( start)


	#make multiple generations
	for gen in range(max_gens):

		t1=time.clock()

		#iterating through grid and calculating live and death statements
		live_state=np.zeros([xm,ym])

		#read first cell position
		firstx= np.min(np.where( grid == 1)[0])-2
		firsty= np.min(np.where( grid == 1)[1])-2
		lastx = np.max(np.where( grid == 1)[0])+2
		lasty = np.max(np.where( grid == 1)[1])+2
		if lastx>99:
			lastx=99
		if lasty>99:
			lasty=99

		#iterate cell elemts
		for i in range(firstx,lastx):
			for j in range(firsty,lasty):
				if i>0 and j>0:
					try:
						a=grid[i-1:i+2,j-1:j+2]
					except:
						a=grid[i-1:,j-1:]
					live_state[i,j]=f(a)



		#making above calculations to new state in the grid
		grid                  = live_state
		number_of_cells[gen]  = np.sum(grid)
		master[gen]           = grid
		last_diff             = np.diff(number_of_cells)[gen-4:gen]

		if np.sum(live_state) == 0:# or len(np.where(last_diff==0))==4:
			print( "All cells died or are stationary")
			break

	print( "**Finished after %s sec**" %(str(round(time.clock()-t1,4))))
	
	if number_of_cells[-1]>number_of_cells[0]:
		plt.figure()	#figure for number of cells
		plt.plot(np.diff(number_of_cells))
		plt.figure()
		plt.plot(number_of_cells)
		plt.show()
		break

if n!=300:
	for grid in master:
		plt.cla()
		plt.imshow(grid,interpolation="nearest")
		plt.grid(False)
		plt.pause(0.001)

	print( "Used starting condition:")
	print( start)

