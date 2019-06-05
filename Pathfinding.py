"""
My try at a pathfinding algorithm. It plots the steps live.

created by Dario Niermann
2017
"""

if True:
	# -*- coding: utf-8 -*-
	print( "Starting...")
	import numpy as np
	import numpy.random as rnd
	import matplotlib.pyplot as plt
	import matplotlib.image as img
	# import scipy.ndimage.filters as filters
	# import pandas as pd
	import os,time
	from math import exp,sqrt,sin,pi,cos,log
	
	np.set_printoptions(precision=3)
	# plt.style.use('ggplot')
	
	
	
	os.chdir(r"C:\Users\dniermann\Downloads\Projects")
	
	from Logger import *
	log=Logger(False)
	log2=Logger(True)
	
	print( u"Finished importing")

######################################################
start_x,start_y=20,20

goal_x,goal_y=50,50

max_x,max_y=100,100

world=img.imread("world.png")[:,:,0]
world=abs(world-1)
# world[4,4]=1
# world[4,5]=1
# world[3,4]=1
# world[2,4]=1
# world[1,4]=1
# world[0,4]=1
# world[4,3]=1
# world[4,2]=1
# world[4,1]=1
# world[4,0]=1

Nodes=[]
world[goal_x,goal_y]=2

######################################################

def manhattan(x1,y1,x2=goal_x,y2=goal_y):
	"""calculates manhattan distance between two points"""
	return abs(x2-x1)+abs(y2-y1)

def find_neighbour(x,y):
	return [[x-1,y-1],[x-1,y+1],[x+1,y-1],[x,y-1],[x-1,y],[x,y+1],[x+1,y],[x+1,y+1]]


def nd_array_sort_col(a,col):
	#sortiert a aber zerstoert a auch nach columns
	m=0
	global b
	b=[]
	found=[]
	while m<len(a):
		save=10.0**10
		n=0
		save2=0
		while n<len(a):
			if a[n][col]<save:
				save=a[n][col]
				save2=a[n]
				found=np.array(save2).tolist()
				save3=n
			n+=1
		b.append(found)
		a[save3]=[10**10,10**10,10**10]
		m+=1
	return b

class Node(object):
	def __init__(self,x,y):
		self.x=x
		self.y=y
		self.walkable=True
		self.listed=False
		self.checked=False

def main_walk(start_x,start_y,goal_x,goal_y,world):
	local_world=np.copy(world)
	#list of nodes to be checked for possible neighbours
	check_nodes=[[start_x,start_y,manhattan(start_x,start_y)]]
	goal_found=False
	checked_nodes=[]

	log2.start("Mainloop")
	while len(check_nodes)>0:
		min_dist=1e10
		Node_i=check_nodes[0]
		local_world[Node_i[0],Node_i[1]]=3
		checked_nodes.append([Node_i[0],Node_i[1]])
		check_nodes.pop(0)
		# log.info("checking Node:",Node_i)
		for i in find_neighbour(Node_i[0],Node_i[1]):
			x=i[0]
			y=i[1]
			
			if x>=0 and x<max_x and y>=0 and y<max_y:
				new=[x,y,manhattan(x,y)]

				if local_world[x,y]==0 or local_world[x,y]==2: #and new not in check_nodes
					# log.out("adding:",x,y)
					check_nodes.append(new)
					local_world[x,y]=0.5
					
					if x==goal_x and y==goal_y:
						# log.out("goal found")
						goal_found=True
						checked_nodes.append([goal_x,goal_y])

		plt.cla()
		plt.imshow((local_world),interpolation="nearest")
		plt.grid(False)
		plt.pause(0.001)

		check_nodes=nd_array_sort_col(check_nodes, 2)
			
		# if len(check_nodes)>0:
		# 	if check_nodes[0][2]<min_dist:
		# 		min_dist=check_nodes[0][2]
		# 		log.out("skipping  because close node was found")
		# 		break
			

		if goal_found==True:
			break

		# log.reset()

	log2.end()
	return checked_nodes

def reverse_walk(checked_nodes,world):
	local_world=np.copy(world)
	log.start("reverse_walk")
	valid_nodes=[]
	max_steps=1000
	log2.start("reverse search")
	if len(checked_nodes)>0:
		n=1
		start_x=checked_nodes[-1][0]
		start_y=checked_nodes[-1][1]


		node=[start_x,start_y]

		
		for step in range(max_steps):
			step2=step
			goal=checked_nodes[n]
			log.out(manhattan(node[0], node[1], goal[0], goal[1]))
			begin_dist=manhattan(node[0], node[1], goal[0], goal[1])
			log.out(goal)
			node=[start_x,start_y]
			
			while node[0]>=0 and node[0]<max_y and node[1]>=0 and node[1]<max_y:
				
				if manhattan(node[0], node[1], goal[0], goal[1])<3:
					if goal[0]>node[0]:
						node[0]+=1
					elif goal[0]<node[0]:
						node[0]-=1
					# if local_world[node[0],node[1]]==1:
					# 	log.info("hit wall")
					# 	local_world=np.copy(world)
					# 	n+=1
					# 	break
					# else:
					# 	local_world[node[0],node[1]]=0.2
					if goal[1]>node[1]:
						node[1]+=1
					elif goal[1]<node[1]:
						node[1]-=1
					if local_world[node[0],node[1]]==1:
						log.info("hit wall")
						local_world=np.copy(world)
						n+=1
						break
					else:
						local_world[node[0],node[1]]=0.2
				else:
					dist1=abs(node[0]-goal[0])
					dist2=abs(node[1]-goal[1])
					if dist2>0:
						ratio=int(dist1/dist2)
					else:
						ratio=1
					#this direction needs to be multiplied by ratio
					switch=False
					for i in range(ratio):
						if goal[0]>node[0]:
							node[0]+=1
						elif goal[0]<node[0]:
							node[0]-=1
						if local_world[node[0],node[1]]==1:
							log.info("hit wall")
							local_world=np.copy(world)
							if begin_dist>20:
								n+=10
							else:
								n+=1
							switch=True
							break
						else:
							local_world[node[0],node[1]]=0.2
					if switch == True:
						break

					if goal[1]>node[1]:
						node[1]+=1
					elif goal[1]<node[1]:
						node[1]-=1
					if local_world[node[0],node[1]]==1:
						log.info("hit wall")
						local_world=np.copy(world)
						if begin_dist>20:
							n+=10
						else:
							n+=1
						break
					else:
						local_world[node[0],node[1]]=0.2

				if node[0]==goal[0] and node[1]==goal[1]:
					start_x=goal[0]
					start_y=goal[1]
					if goal not in valid_nodes:
						valid_nodes.append(goal)
					log.info("touched goal",goal)
					n=0
					break

				



				# plt.cla()
				# plt.imshow((local_world),interpolation="nearest")
				# plt.grid(False)
				# plt.pause(0.01)

			if node[0]==checked_nodes[0][0] and node[1]==checked_nodes[0][1]:
				log2.out("solution found! ",step)
				break

	log.end()
	print( step2)
	log2.end()
	return valid_nodes
 

my_nodes = main_walk(start_x, start_y, goal_x, goal_y, world)
valid_nodes = reverse_walk(my_nodes,world)
world[start_x,start_y]=0.5
world[goal_x,goal_y]=0.5
for i in valid_nodes:
	world[i[0],i[1]]=0.5
print( valid_nodes)

plt.imshow(world,interpolation="nearest")
plt.grid(False)
plt.show()
