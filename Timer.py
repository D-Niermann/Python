"""
My little simple timer because I didnt find a similar app online, so I made my own.
Just enter how many minutes you want to time.

The sound output at the end does not worl on Windows I guess, I built this as an .app on my macbook and it works finde,
on this PC here it does not work, but im writing this 3 years after I coded this so I dont bother to fix the sound.

Programming this teached me a lot of stuff back then. That what counts.

Created by Dario Niermann
2017
"""

#-*- coding: utf-8 -*-
# import numpy as np
# import seaborn
import threading as thd
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
from os import system
from tkinter import font
# from math import exp,sqrt
from tkinter import *
from sys import exit
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import sleep,time


##################################################################
""" Basic settings"""
root = Tk()
root.wm_title("Timer")


root.customFont = font.Font(family="Helvetica", size=25)
root.customFont2 = font.Font(family="Helvetica", size=140)
root.customFont3 = font.Font(family="Helvetica", size=14)
##################################################################

##################################################################
"""Variables"""
time_seconds=-1
time_seconds_set=-1
start_time=0.
time_perc=1
str_time = StringVar()
alarm_finished=1
str_time.set("00:00")
background_color="#283242"
##################################################################


def close():
	root.destroy()
	exit()

def sek2minutes(sek):
	anz_minuten=int(sek)//60
	anz_sek=abs(anz_minuten*60-sek)
	if anz_minuten<10:
		str_min="0"+str(anz_minuten)
	else:
		str_min=str(anz_minuten)
	if anz_sek>=10:
		return str_min+":"+str(int(anz_sek))
	else:
		return str_min+":"+"0"+str(int(anz_sek))


def get_time(*args):
	global time_seconds,start_time,alarm_finished,time_seconds_set
	if time_seconds>0:
		alarm_finished=1
		time_seconds=0
	else:	
		alarm_finished=0
		try:
			time_seconds = float(eingabe.get("1.0","end"))*60
			time_seconds_set=float(eingabe.get("1.0","end"))*60
			eingabe.delete("1.0","end")
			start_time=time()
		except:
			time_seconds=-1
			time_seconds_set=-1
			eingabe.delete("1.0","end")

		return time_seconds

def main(*args):
	global time_seconds,alarm_finished,time_seconds_set

	while True:
		sleep(0.999)

		time_perc=time_seconds/time_seconds_set

		if time_seconds>=0:
			
			str_time.set(sek2minutes(time_seconds))
			time_seconds-=1.

			canvas.delete(ALL)
			canvas.create_rectangle(0, 0, (w-offset)*time_perc, 20, fill="#ffe9e1")
			# print time_perc

		if time_seconds<0 and alarm_finished==0:
			alarm_finished=1
			for i in range(0,3):
			    system('afplay /System/Library/Sounds/Glass.aiff')
			

##################################################################
"""Tkinter stuff"""
eingabe=Text(root,bg=background_color,height=1,width=10,font=root.customFont3,highlightcolor="#ffe9e1",fg="#ffe9e1",relief=FLAT)
eingabe.focus_set()
#selectbackground
# text = Text(root,bd=0, wrap=WORD,width=180,height=19,font=root.customFont,bg=background_color)


title1=Label(root,text="Timer",font=root.customFont,background=background_color,fg="white")
title2=Label(root,text="Time in Minutes:",font=root.customFont3,background=background_color,anchor=CENTER,fg="#ffe9e1")
counter=Label(root,textvariable=str_time,font=root.customFont2,background=background_color,anchor=CENTER,fg="#ffe9e1")
# title2=Label(root,text="Hier Text eingeben:",font=root.customFont2,background=background_color)
button2=Button(root,text="Start / Stop",background="black",command=get_time)


separator = Frame(height=2, bd=1, relief=SUNKEN)
separator2 = Frame(height=2, bd=1, relief=SUNKEN)

# title1.grid(row=0,column=0,sticky="W") # timer title

counter.grid(row=1,column=0,columnspan=2,padx=100) #countdown

title2.grid(row=2,column=0,sticky="E") #enter time in  minutes
eingabe.grid(row=2,column=1,sticky="W")
# button2.grid(row=2,column=2,sticky="W")


##################################################################
"""Threads"""
Thread1=thd.Thread(target=main,args=())
Thread1.daemon = True
Thread1.start()

##################################################################



##################################################################
# # Add the binding
# text.bind("<Control-Key-a>", select_all)
# text.bind("<Control-Key-A>", select_all) 
eingabe.bind("<Return>", get_time) 
##################################################################

# get screen width and height
ws = root.winfo_screenwidth() # width of the screen
hs = root.winfo_screenheight() # height of the screen

#breite und hoehe des Fensters
w=int(0.373*ws)
h=int(0.24*hs)

offset=20

canvas = Canvas(root, width=w, height=10,bg=background_color,highlightbackground=background_color)
canvas.grid(row=0,column=0,columnspan=2)
canvas.create_rectangle(0, 0, (w-offset)*time_perc, 20, fill="#ffe9e1")
# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.protocol('WM_DELETE_WINDOW', close)
root.configure(background=background_color)

##################################################################
root.mainloop()


