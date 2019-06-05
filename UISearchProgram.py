"""
Search Tool that works like Spotlight for Mac, exept its slower and way more stupid.
Teached myself how to use GUI applications and multiple threads.
change the dir to some location here it is C:// and create a file named "cwds.txt" where you 
have to enter some search directories e.g. C://Users/Name/Documents. Multiple paths can be added
and need to be comma seperated. A COMMA IS ALWAYS NEEDED EVEN IF JUST ONE PATH IS ENTERED.

After that start the Program and you can type in your searchwork.

Formatting here is very bad, also not commented, i feel ashamed for my old self.

Also the programm does not terminate itself correctly after opening a file.

Created by: Dario Niermann
Created around 2016
"""


import tkinter as tk
from tkinter import font, filedialog
import sys
# import numpy as np
import os
import time
import subprocess
import threading as thd


## change this path for your liking, here some config files will be created.
os.chdir("C:\\Users\\dniermann")

def close_win(self):
     sys.exit(0)
searchword_save=""
results0=[]
results=[]
results2=[]
final_string=""
cwds=[]
save_pos=0
show_lenght=30
textfield_pos=0
show_list=[]
butt_press=0

def search(self):
    global save_pos,results,results2,searchword_save,final_string,show_lenght,show_list,butt_press,textfield_pos
    #reading cwds
    file1=open("cwds.txt","r")
    for string in file1:
        for j in range(len(string)):
            if string[j]==",":
                if string[save_pos:j] not in cwds and len(string[save_pos:j])>0:
                    cwds.append(string[save_pos:j])
                    save_pos=j+1
    
    file1.close()
    save_pos=0
            
    trigger=False
    
    searchword=str(MyText.get("1.0","1.end"))
    
    if len(searchword)>1 and searchword!=searchword_save:             
        results0=[]
        results=[]
        results2=[]
        show_list=[]

        if len(cwds)>0:
            for i in cwds:
                c=[]
                try:
                    file3=open("fav.txt","r")
                    for string in file3:
                        for j in range(len(string)):
                            if string[j]==",":
                                if string[save_pos:j] not in c and len(string[save_pos:j])>0:
                                    c.append(string[save_pos:j])
                                    save_pos=j+1
                    file1.close()
                except:
                    pass

                a = [x[0] for x in os.walk(str(i))]
                
                b = []
               
           
                for i in range(len(a)):
                    b.append([[a[i]],[x for x in os.listdir(a[i]) if "." in x]])
              
                
                #search folders
                for i in range(len(c)):
                    for j in range(1,len(c[i])+1):
                        print(c[i][-j] )
                        if c[i][-j]=="/":
                            save=len(c[i])+1-j
                            break
                    try:
                        if searchword.lower() in c[i][save:len(c[i])].lower() and len(results)<show_lenght/3:
                            results.append([c[i],c[i][save:len(c[i])]])
                    except:
                        pass    

                # for i in range(len(a)):
                #     for j in range(1,len(a[i])+1):
                #         if a[i][-j]=="/":
                #             save=len(a[i])+1-j
                #             break
                #     if searchword.lower() in a[i][save:len(a[i])].lower() and len(results)<show_lenght/3:
                #         results.append([a[i],a[i][save:len(a[i])]])
                        
                print(results)
                # if len(results)>=1:
                #     print( "\n Folders:")
                #     for i in range((show_lenght)):
                #         try:
                #             print( "#"+str(i+1)+":"+" "+results[i][1] )
                #         except:
                #             pass
                # else:
                #     print "---------------------"
                #     print "No Folders found"
                #     MyText2.delete("1.0","end")

                n=0
                #search files
                for i in range(len(b)):
                    while True:
                        try:
                            if searchword.lower() in b[i][1][n].lower() and len(results2)<show_lenght/3:
                                results2.append([b[i],b[i][1][n]])
                        except:
                            n=0
                            break
                        n+=1

                #create finalstring 
                if 0<len(results):
                    final_string=str(results[browse_n][0])
                elif 0<len(results2):
                    final_string=str(results2[browse_n-len(results)][0][0][0]+"/"+str(results2[browse_n-len(results)][1]))


                if trigger==False and len(results2)>=1:
                    print( "\n Files:")
                    for i in range((show_lenght)):
                        try:
                            print("#"+str(i+len(results)+1)+":"+" "+results2[i][1])
                        except:
                            pass
                else:
                    print("No Files Found")
        searchword_save=searchword
    


    for i in results:
        if i[1] not in show_list:
            show_list.append(i[0])
    for i in results2:
        if i[1] not in show_list:
            show_list.append(i[1])        
    try:
        MyText2.delete("1.0","end")
        MyText2.insert("1.0",show_list[textfield_pos+butt_press])
    except:
        pass
    try:
        MyText3.delete("1.0","end")
        MyText3.insert("1.0",show_list[textfield_pos+1+butt_press])
    except:
        pass
    try:
        MyText4.delete("1.0","end")
        MyText4.insert("1.0",show_list[textfield_pos+2+butt_press])
    except:
        pass
def search_refresh():
    while True:
        search(self)
        time.sleep(0.3)
Thread1=thd.Thread(target=search_refresh,args=())
Thread1.daemon = True


def start_new(self):
    self=tk.Tk()
    self.overrideredirect(True)
    self.customFont = font.Font(family="Calibri", size=18)
    self.mCan = tk.Canvas(self, height=100, width=500)
    self.mCan.pack()
    self.mainloop()


browse_n=-1
def browse_d(self):
    global final_string,browse_n,results,results2,textfield_pos,butt_press
    butt_press+=1
    browse_n+=1
    if browse_n+1<len(results):
        final_string=str(results[browse_n+1][0])
    else:
        final_string=str(results2[browse_n+1-len(results)][0][0][0]+"/"+str(results2[browse_n+1-len(results)][1]))
    
def browse_u(self):
    global final_string,browse_n,results,results2,textfield_pos,butt_press
    butt_press-=1
    browse_n-=1
    if browse_n+1<len(results) and browse_n+1>=0:
        final_string=str(results[browse_n+1][0])
    else:
        final_string=str(results2[browse_n+1-len(results)][0][0][0]+"/"+str(results2[browse_n+1-len(results)][1]))


def open_file(self):
    global final_string,results,results2
    MyText.delete("1.0","end")
    results=[]
    results2=[] #if final_string==len=0 dann einmal runter gehen und das erste result offnen
    os.popen(final_string.replace("\\","/"))
    sys.exit()

def get_cwd(self):
    global cwds
    cwds.append(str(MyText.get("1.0","1.end")))
    file1=open("cwds.txt","w")
    for i in cwds:
        file1.write(str(i)+",")
    file1.close()
    MyText.delete("1.0","end")

def get_showlenght(self):
    global show_lenght
    show_lenght=int(str(MyText.get("1.0","1.end")))
    MyText.delete("1.0","end")


self = tk.Tk()
# self.overrideredirect(True)
self.customFont = font.Font(family="Calibri", size=18)
self.customFont2 = font.Font(family="Calibri", size=10)
self.mCan = tk.Canvas(self, height=0, width=500)
self.mCan.pack()


MyText = tk.Text(self,height=1,width=42,padx=30,spacing1=10,spacing3=10 ,font=self.customFont,bd=0,bg="#ffffff")
MyText.pack()
MyText.focus_set()

MyText2 = tk.Text(self,height=1,width=77,padx=30,spacing1=5,spacing3=5 ,font=self.customFont2,bd=0,bg="#ddffdd")
MyText2.pack()
MyText3 = tk.Text(self,height=1,width=77,padx=30,spacing1=5,spacing3=5 ,font=self.customFont2,bd=0,bg="#dddddd")
MyText3.pack()
MyText4 = tk.Text(self,height=1,width=77,padx=30,spacing1=5,spacing3=5 ,font=self.customFont2,bd=0,bg="#dddddd")
MyText4.pack()

# Binds
self.bind('<Escape>', close_win)
self.bind("<Return>", open_file)
self.bind('<Down>',browse_d)
self.bind("<Up>",browse_u)
self.bind("<F1>",get_cwd)
self.bind("<F2>",get_showlenght)
# Center the window
self.update_idletasks()
xp = (self.winfo_screenwidth() / 2) - (self.winfo_width() / 2)
yp = (self.winfo_screenheight() / 2) - (self.winfo_height() / 2)-200
# self.geometry('{0}x{1}+{2}+{3}'.format(self.winfo_width(),self.winfo_height(),xp, yp))


Thread1.start()

self.mainloop()


""" results lsiten auf show_lenght lenge einrichten und dann keine append befehle mer nutzen die 
sollten eigtl nicht mehr funktinoieren mit dem thread jetzt

deshalb fuhrt zu langes hin und her suchen nicht mehr zu ergebnissen


F3 suchtiefe
es sollten auch bei files die anfangsbuchstaben hoher priorisiert sein.. also bei suche nach "test" sollte nicht erst "kepler test" kommen 

alle unterordner in file speichern so bei vielen ordnern das programm nicht zum starten lange laden muss...zum starten brauch das nicht mehr lange

alle files die jemals geoffnet wurden in eine txt schreiben mit pfad und so und dann zu erst die durchsuchen und in results und results2 schreiben
"""

