"""
Image manipulation tool.

Created by: Dario Niermann
Created around 2015
"""

import matplotlib.pyplot as plt
import matplotlib.image as mi
import numpy as np
import os as os
import time 

print( "############################### Niermann GmbH ###############################")
print( "")
print( "############# Super fancy picture changing algorithms by Me #############")
print( "")
print( "List of coises:")
print( "1. Greyscale")
print( "2. Blur")
print( "3. Change Brightness")
print( "4. Convert")
print( "5. Change dir")
print( "6. Bloom")
print( "9. Quit")
print( "")
n=0
m=0
# os.chdir("C:\Users\Ann-Marie Parrey\Google Drive\Praktikum")
cwd=os.getcwd()
print( "Current directory: %s" %cwd)
while n<1:
	enter=input("What is your choise: ")

	if enter=="Greyscale" or (enter)=="1":
		filename=input("Enter Filename:  ")

		while m<1:
			try:
				img=mi.imread(filename)
				m=1
				print( "File read succesfully!")
			except:
				print( "Error: No such file found!")
				print( os.listdir())
				filename=input("Enter Filename:  ")
		
		for i in range(100):
			for j in range(100):
				save=(img[i,j,0]*0.3+img[i,j,1]*0.6 +img[i,j,2]*0.11)
				
				for k in range(3):
					
					img[i,j,k]=save
		enter3=input("Show Image?  ")
		if enter3=="Yes" or enter3=="y":
			plt.imshow(img)
			plt.show()		
	

		enter2=input("Save Image?  ")

		if enter2=="Yes" or enter2=="y":
			img_name=input("Imagename: ")
			fig = plt.figure(frameon=False)
			ax = plt.Axes(fig, [0., 0., 1., 1.])
			ax.set_axis_off()
			fig.add_axes(ax)
			ax.imshow(img)
			fig.savefig(img_name)
			print( "There you go!")
		m=0

	elif str(enter)=="Blur" or (enter)=="2":
		filename=input("Enter Filename:  ")

		while m<1:
			try:
				img=mi.imread(filename)
				m=1
				print( "File read succesfully!")
			except:
				print( "Error: No such file found!")
				filename=input("Enter Filename:  ")
		
		strength=input("Enter Effectstrength:  ")
		
		for n in range(int(strength)):
			for i in range(img.shape[0]):
				for j in range(img.shape[1]):
					if i>0:
						try:
							save1=img[i-1,j,:]
						except:
							None
					if j<img.shape[1]:
						try:
							save2=img[i,j+1,:]
						except:
							None
					if i<img.shape[0]:
						try:
							save3=img[i+1,j,:]
						except:
							None
					if j>0:
						try:
							save4=img[i,j-1,:]
						except:
							None
					try:
						img[i,j,:]=(save1+save2+save3+save4)/4		
					except:
						None
		enter3=input("Show Image?  ")
		if enter3=="Yes" or enter3=="y":
			plt.imshow(img)
			plt.show()		
		

		enter2=input("Save Image?  ")

		if enter2=="Yes" or enter2=="y":
			img_name=input("Imagename: ")
			fig = plt.figure(frameon=False)
			ax = plt.Axes(fig, [0., 0., 1., 1.])
			ax.set_axis_off()
			fig.add_axes(ax)
			ax.imshow(img)
			fig.savefig(img_name)
			print( "There you go!")
		else:
			None

	elif enter=="3" or enter=="Change Brightness":
		filename=input("Enter Filename:  ")

		while m<1:
			try:
				img=mi.imread(filename)
				m=1
				print( "File read succesfully!")
			except:
				print( "Error: No such file found!")
				filename=input("Enter Filename:  ")


		strength=input("Enter Effectstrength (between -1 and 1): ")
		
		for i in range(img.shape[0]):
			for j in range(img.shape[1]):
				for k in range(3):
					if float(strength)>0:
						if img[i,j,k]+float(strength)<=1 :
							img[i,j,k]=img[i,j,k]+float(strength)
						else:
							img[i,j,k]=1
					if float(strength)<0:
						if img[i,j,k]-abs(float(strength))>=0:
							img[i,j,k]=img[i,j,k]-abs(float(strength))
						else:
							img[i,j,k]=0
		enter3=input("Show Image?  ")
		if enter3=="Yes" or enter3=="y":
			plt.imshow(img)
			plt.show()		
	

		enter2=input("Save Image?  ")

		if enter2=="Yes" or enter2=="y":
			img_name=input("Imagename: ")
			fig = plt.figure(frameon=False)
			ax = plt.Axes(fig, [0., 0., 1., 1.])
			ax.set_axis_off()
			fig.add_axes(ax)
			ax.imshow(img)
			fig.savefig(img_name)
			print( "There you go!")
		m=0
	elif enter=="4" or enter=="Convert" or enter=="convert":
		filename=input("Enter Filename:  ")

		while m<1:
			try:
				img=mi.imread(filename)
				m=1
				print( "File read succesfully!")
			except:
				print( "Error: No such file found!")
				filename=input("Enter Filename:  ")
			
		img_name=input("Convert to (with filename): ")
		fig = plt.figure(frameon=False)
		ax = plt.Axes(fig, [0., 0., 1., 1.])
		ax.set_axis_off()
		fig.add_axes(ax)
		ax.imshow(img)
		fig.savefig(img_name)
		print( "There you go!")
		m=0
	elif enter=="5":
		enter2=input("New Directory:")
		os.chdir(enter2)
		cwd=os.getcwd()
		print( "New Directory: %s" %cwd)
	elif enter=="6":
		filename=input("Enter Filename: ")
		while m<1:
			try:
				img=mi.imread(filename)
				m=1
				print( "File read succesfully!")
			except:
				print( "Error: No such file found!")
				filename=input("Enter Filename:  ")

		img2=np.zeros([img.shape[0],img.shape[1]])

		for i in range(img.shape[0]):
			for j in range(img.shape[1]):
				a=int(10*np.sum(img[i,j][:]))
				try:
					img2[i-a:i+a,j-a:j+a][:]=np.multiply(img[i-a:i+a,j-a:j+a][:],1.2)
				except:
					pass

		enter3=input("Show Image?  ")
		if enter3=="Yes" or enter3=="y":
			plt.imshow(img2,interpolation=None)
			plt.show()	

	elif enter=="9" or enter=="quit":
		n=1

	else:
		print( "No valid choise!")

	