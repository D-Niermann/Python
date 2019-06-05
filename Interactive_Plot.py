""" 
Simple tool for plotting a function f(x) over x given 3 parameters which can be changed interactivley

Created by Dario Niermann
2016
"""

#-*- coding: utf-8 -*-
print( "Starting...")
import numpy as np
import threading as thd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter import Tk,Text,Entry,Scale,HORIZONTAL,INSERT,END,WORD,Checkbutton,DoubleVar,IntVar,DISABLED,Label,SEL,BOTH,X,Frame,SUNKEN,VERTICAL,font
from sys import exit
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import sleep,clock
from math import pi
#################################################################################

#Plot
str_title=u""
x_label=u"x"
y_label=u"y"

#Function for linplot
lin=1
def logistic(x,a):
	y0 = 0.005
	y = np.zeros(shape=len(x))
	y[0] = y0
	for i in range(1,len(x)):
		y[i] = (1-y[i-1])*a*0.01
	return y




""" enter your function here, f(x_array; a,b,c) given parameters a,b,c"""
def function(x_array,a,b,c):
	return np.sin(x_array*a*0.1)*0.1*b+c*0.1




#Function for matplot
mat=0
def function_mat(x,y,a,b,c):
	return x*(y-10)*a

x_array=np.linspace(0,100,1000)
y_array=np.linspace(0,100,1000)
#Variable Range
a_min,a_max=0,100
b_min,b_max=0,100
c_min,c_max=0,100

##################################################################################


root = Tk()
root.wm_title("Plot")
root.configure(background='white')

root.customFont = font.Font(family="Sans Serif", size=12)
root.customFont2 = font.Font(family="Calibri", size=15)

eingabe=Scale(root,bg="white",label="Variable a",orient=HORIZONTAL,length=300,from_=a_min,to=a_max,width=30,font=root.customFont,highlightcolor="white")
eingabe4=Scale(root,bg="white",label="Variable b",orient=HORIZONTAL,length=300,from_=b_min,to=b_max,width=30,font=root.customFont,highlightcolor="white")
eingabe5=Scale(root,bg="white",label="Variable c",orient=HORIZONTAL,length=300,from_=c_min,to=c_max,width=30,font=root.customFont,highlightcolor="white")

eingabe2=Scale(root,bg="white",label="Y-Skale",orient=HORIZONTAL,length=300,from_=1,to=100,width=30,font=root.customFont,highlightcolor="white")
eingabe3=Scale(root,bg="white",label="X-Skale",orient=HORIZONTAL,length=300,from_=1,to=100,width=30,font=root.customFont,highlightcolor="white")

eingabe.pack()
eingabe4.pack()
eingabe5.pack()
eingabe2.pack()
eingabe3.pack()

eingabe.set(1)
eingabe4.set(1)
eingabe5.set(1)
eingabe2.set(10)
eingabe3.set(10)

xx21=x_array
if lin==1:
	func=function(xx21,1,1,1)
elif mat==1:
	func=np.zeros([len(x_array),len(y_array)])

fig1 = plt.figure(figsize=(5,3.5))
ax = fig1.add_subplot(111)
plt.subplots_adjust(bottom=0.2)



def close():
	root.destroy()
	exit()

var1=DoubleVar()
var1.set(1.)
var2=DoubleVar()
var2.set(1.)
var3=DoubleVar()
var3.set(1.)
var4=DoubleVar()
var4.set(1.)
var5=DoubleVar()
var5.set(1.)

def get_var():
	global xx21,var2,var3,func
	var3_save=0
	var4_save=0
	var5_save=0
	while True:
		if lin==1:
			sleep(0.05)
		elif mat==1:
			sleep(0.2)
		try:
			var1.set(eingabe3.get())
			var2.set(eingabe2.get())
			var3.set(eingabe.get())
			var4.set(eingabe4.get())
			var5.set(eingabe5.get())
		except:
			pass
		# xx21=np.linspace(0,var3.get()*pi,1000)
		if var3.get()!=var3_save or var4.get()!=var4_save or var5.get()!=var5_save:
			if lin==1:
				func=function(xx21,var3.get(),var4.get(),var5.get())
			elif mat==1:
				for i in range(len(x_array)):
					for j in range(len(y_array)):
						func[i,j]=function_mat(i,j,var3.get(),var4.get(),var5.get())
			var3_save=var3.get()
			var4_save=var4.get()
			var5_save=var5.get()



max_y=1
max_x=1
min_x=1
if lin==1:
	line, = ax.plot([], [],linewidth=2)
def animate_lin(i):
	global min_x,max_x,max_y,xx21,func,var2
	var1_save,var2_save,var3_save=0,0,0
	if var1.get()!=var1_save or var2.get()!=var2_save or var3.get()!=var3_save:
		# ax.clear()
		# ax.plot(xx21,func,"r-")
		line.set_data(xx21, func)
		if i<5:
			max_y=max(func)
			max_x=max(xx21)
			min_x=min(xx21)
		ax.set_ylim([-max_y*var2.get()*0.1,max_y*var2.get()*0.1])
		ax.set_xlim([-min_x*var1.get()*0.1,max_x*var1.get()*0.1])
		plt.ylabel(y_label)
		plt.xlabel(x_label)
		plt.title(str_title)
		var1_save,var2_save,var3_save,var4_save,var5_save=var1.get(),var2.get(),var3.get(),var4.get(),var5.get()
	return line,

def animate_mat(i):
	global min_x,max_x,max_y,xx21,func,var2
	var1_save,var2_save,var3_save=0,0,0
	if var1.get()!=var1_save or var2.get()!=var2_save or var3.get()!=var3_save:
		ax.clear()
		ax.matshow(func,clim=(0,max_y*var2.get()*0.1))
		if i<5:
			max_y=np.max(func)
		plt.ylabel(y_label)
		plt.xlabel(x_label)
		plt.title(str_title)
		var1_save,var2_save,var3_save,var4_save,var5_save=var1.get(),var2.get(),var3.get(),var4.get(),var5.get()



Thread1=thd.Thread(target=get_var,args=())
Thread1.daemon = True
Thread1.start()


canvas = FigureCanvasTkAgg(fig1,root)
canvas.get_tk_widget().configure(background="white")
canvas.get_tk_widget().pack(fill=BOTH,expand=True)
if lin==1:
	ani = animation.FuncAnimation(fig1,animate_lin, interval=50)
elif mat==1:
	ani = animation.FuncAnimation(fig1,animate_mat, interval=500)


# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

#breite und hoehe des Fensters
w=int(0.8*ws)
h=int(0.8*hs)

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.protocol('WM_DELETE_WINDOW', close)


root.mainloop()

