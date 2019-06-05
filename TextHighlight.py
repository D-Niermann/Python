"""
Programm that searches for duplicate sentence beginnings and marks them. For controlling your own written texts for redundancy

Created by Dario Niermann
2017
"""

#-*- coding: utf-8 -*-
print( "Starting...")
# import numpy as np
import seaborn
import threading as thd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# from math import exp,sqrt
# print( u"Finished importing")
from tkinter import Tk,Text,INSERT,END,WORD,Checkbutton,IntVar,DISABLED,Label,SEL,BOTH,X,Frame,SUNKEN,font
from sys import exit
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from time import sleep


root = Tk()
root.wm_title("TextHighlighter")
root.configure(background='white')
button_var = IntVar()
button_var.set(1)
button_var2 = IntVar()

root.customFont = font.Font(family="Sans Serif", size=12)
root.customFont2 = font.Font(family="Calibri", size=15)

button=Checkbutton(root,text="Satz- und Nebensatzanfänge zeigen",variable=button_var,onvalue=1,offvalue=0,background="white")
button2=Checkbutton(root,text="Hintergrund Aktuallisierung",variable=button_var2,onvalue=1,offvalue=0,background="white")

eingabe=Text(root,bg="white",height=2,width=180,font=root.customFont,highlightcolor="white")
#selectbackground
text = Text(root,bd=0, wrap=WORD,width=180,height=19,font=root.customFont,bg="white")
text.insert(END,u'Es ist ein lang erwiesener Fakt, dass ein Leser vom Text abgelenkt wird, wenn er sich ein Layout ansieht. Der Punkt, Lorem Ipsum zu nutzen, ist, dass es mehr oder weniger die normale Anordnung von Buchstaben darstellt und somit nach lesbarer Sprache aussieht. Viele Desktop Publisher und Webeditoren nutzen mittlerweile Lorem Ipsum als den Standardtext, auch die Suche im Internet nach "lorem ipsum" macht viele Webseiten sichtbar, wo diese noch immer vorkommen. Mittlerweile gibt es mehrere Versionen des Lorem Ipsum, einige zufällig, andere bewusst (beeinflusst von Witz und des eigenen Geschmacks).')
title1=Label(root,text="Hier Suchwörter eingeben:",font=root.customFont2,background="white")

title2=Label(root,text="Hier Text eingeben:",font=root.customFont2,background="white")


separator = Frame(height=2, bd=1, relief=SUNKEN)
separator2 = Frame(height=2, bd=1, relief=SUNKEN)
separator3 = Frame(height=2, bd=1, relief=SUNKEN)
separator4 = Frame(height=2, bd=1, relief=SUNKEN)

button.pack()
# button2.pack()
title1.pack(anchor="w")
# separator.pack(fill=X, padx=5, pady=5)
eingabe.pack()
separator2.pack(fill=X, padx=5, pady=5)
title2.pack(anchor="w")
# separator3.pack(fill=X, padx=5, pady=5)
text.pack()
# separator4.pack(fill=X, padx=5, pady=5)





f = plt.figure(figsize=(5,3.5))
ax = f.add_subplot(111)
plt.subplots_adjust(bottom=0.2)
plt.title(u"Anzahl der Sätze und Dublikate")

array={}

def close():
	root.destroy()
	exit()



def select_all(event):
    text.tag_add(SEL, "1.0", END)
    text.mark_set(INSERT, "1.0")
    text.see(INSERT)
    return 'break'


def animate(i):
	global array
	if len(array)>1:
		try:
			array[u"#Sätze"]=array.pop(". ")
			array[u"#Nebensätze"]=array.pop(", ")
		except:
			pass
		ax.clear()
		ax.bar(range(0,len(array)*2,2),array.values(),width=1.2)
		plt.ylabel(u"Anzahl")
		plt.title(u"Anzahl der Sätze und Dublikate")
		plt.xticks(range(0,len(array.keys())*2,2),array.keys(),rotation=30.)
	else:
		ax.clear()
		plt.ylabel(u"Anzahl")
		plt.title(u"Anzahl der Sätze und Dublikate")
		plt.xticks(range(20),[""]*20)



canvas = FigureCanvasTkAgg(f,root)
canvas.get_tk_widget().configure(background="white")
canvas.get_tk_widget().pack(fill=BOTH,expand=True)
ani = animation.FuncAnimation(f,animate, interval=1000)


color_table=["red","yellow","#e39661","#dbe361","#93e361","#61e3b2","#61cce3","#6163e3","#c861e3","#e361a3","#e36161"]
def get_text():
	global text,eingabe,color_table,button_var,array,button_var2,canvas
	t      = []
	t_old  = []
	e_     = []
	switch = 0
	tags   = []
	e_old  = []


	# canvas.draw()
	

	while True:
		sleep(0.5)

		#get user input ###################################################
		try:
			t=text.get("1.0","end")
			e_=eingabe.get("1.0","end")
		except:
			exit(0)

		
		##########
		e=[". ",", "]
		save=0
		color=0
		satzanfang=-1
		wortende=-1
		##########


		# search for sentence beginnings ####################################
		if button_var.get()==1:
			punkt=map(lambda x: 1 if x=="." else 0,t)
			leer=map(lambda x: 1 if x==" " else 0,t)
			komma=map(lambda x: 1 if x=="," else 0,t)
			# bs=map(lambda x: 1 if x=="\\" else 0,t)
			try:
				for k in range(4,len(punkt)):
					if punkt[k]==1 and leer[k+1]==1 and punkt[k-3]!=1 and punkt[k-2]!=1 and punkt[k-1]!=1:
						satzanfang=k+2
						for kk in range(len(punkt[satzanfang:])):
							if leer[satzanfang+kk]==1:
								wortende=satzanfang+kk+1
								if t[satzanfang:wortende] not in e:
									e.append(t[satzanfang:wortende])
								break
					elif komma[k]==1 and leer[k+1]==1:
						satzanfang=k+2
						for kk in range(len(punkt[satzanfang:])):
							if leer[satzanfang+kk]==1:
								wortende=satzanfang+kk+1
								if t[satzanfang-2:wortende] not in e:
									e.append(t[satzanfang-2:wortende])
								break	
			except:
				pass
		
		for i in range(len(e)):
			if e[i].isalpha()==False:
				e[i]=''.join([j for j in e[i] if j.isalpha() or j==" " or j=="." or j==","])



		# slice input of e_ in arraytype #####################################
		if len(e_)>1:
			
			for i in range(len(e_)):
				if e_[i]==",":
					e.append(e_[save:i])
					save=i+1
				elif i==len(e_)-1:
					e.append(e_[save:])
			
			e[-1]=e[-1][:-1]


		# mark all words in e that are more than once ###################################
		if e!=e_old or len(t)!=len_t:
			for j in tags:
				text.tag_delete(j)
			# text.tag_add("all","1.0","end")
			# text.tag_config("all",background="white")
			array={}
			for searchword in e:
				if len(searchword)>1:
					pos=[]
					start=1.0
					while 1:
						try:
							p=text.search(searchword, start, stopindex=END)
						except:
							pass
						if len(p)>1:
							pos.append((p,p+"+%ic"%len(searchword)))
						if not p:
							break
						start = p + "+1c"

					try:
						if len(pos)>1:
							array.update({str(searchword):len(pos)})
					except:
						print( "error")

					if len(pos)>1:
						for i in pos:	
							text.tag_add(searchword,i[0],i[1])
							tags.append(searchword)
							text.tag_config(searchword,background=color_table[color])

						if color<len(color_table)-1:
							color+=1
						else:
							color=0
			
			e_old=e
			animate(1)
			try:
				len_t=len(t)
			except:
				pass


Thread1=thd.Thread(target=get_text,args=())
Thread1.daemon = True


# Add the binding
text.bind("<Control-Key-a>", select_all)
text.bind("<Control-Key-A>", select_all) 
text.bind("<Control-Key-s>", get_text) 


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


print("Starting thread")
Thread1.start()

root.mainloop()
