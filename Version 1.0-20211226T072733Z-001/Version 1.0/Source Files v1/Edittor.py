from tkinter import *
from tkinter import filedialog
from cv2 import *
import numpy as np
import cv2
import comm



def addDef():

     T2.delete("1.0","end")
     T2.insert(END, "1")
     T3.delete("1.0","end")
     T3.insert(END, "12")

def draw(arr,s):
     
     cv2.line(imm,(arr[1][0],arr[1][1]),(arr[0][0], arr[0][1]), (57, 255, 20), 1)
     cv2.imshow('Hold \'SPACE\' to Draw or \'B\' to Quit ',imm) 
     cv2.waitKey(s)



def visGcode(fileO):

     global imm
     imm=np.zeros((600,600,3),np.uint8) 
     file = open(fileO+"/output.gcode", "r")
     x,y=0,0
     buffer=[]
     S=int(T2.get(1.0, "end-1c"))
     Z=float(T3.get(1.0, "end-1c"))

     while True:

          line = file.readline()
          if line[0:3]=="M18" or line==False: break
         
          if(line[0]=='G'):
        
               indx=line.find('X')
               indy=line.find('Y')
               x=int(float(line[indx+1:indy-1])*Z)
               y=int(float(line[indy+1:indy+5])*Z)
               buffer.append([x,y])
               if(len(buffer)==2):
                    draw(buffer,S)
                    buffer.pop(0)
    
          if(line[5:8]=="S50" and line[0]=="M"):
               up=True
               if(len(buffer)==1):
                    buffer.append([buffer[0][0],buffer[0][1]])
                    draw(buffer,S)
               buffer=[]

          
               
     cv2.waitKey(0)
     cv2.destroyAllWindows()
     file.close()

def CommSell(d,fileO):

    ws.destroy()
    comm.ComSel(d,fileO)

def fileReader(fileO,dim=40):

    global textarea,T2,T3,ws

    ws = Tk()
    ws.title("Gcode Generated")
    ws.resizable(False, False)
    ws['bg']='#4aa96c'

    Label(ws, text ="G-code File", font=('Arial',20,'bold'),foreground="White"
            ,background="#4aa96c").pack(pady = 5)
    canvas2 = Canvas(ws, width =200, height =-2) 
    canvas2.pack(fill=BOTH,expand=1,pady=2)
    canvas2 = Canvas(ws, width =200, height =-2) 
    canvas2.pack(fill=BOTH,expand=1,pady=2)          
    # adding frame
    frame = Frame(ws)
    frame.pack(pady=10,padx=10)
    # adding scrollbars 
    ver_sb = Scrollbar(frame, orient=VERTICAL)
    ver_sb.pack(side=RIGHT, fill=BOTH)
    # adding writing space
    txtarea = Text(frame, width=50, height=30,background="black",foreground="#39FF14",font=('Courier',11,'bold'))
    txtarea.pack()
    # binding scrollbar with text area
    txtarea.config(yscrollcommand=ver_sb.set)
    ver_sb.config(command=txtarea.yview)

    # calling the function
    tf = open(fileO+"/output.gcode")
    file_cont = tf.read()
    txtarea.insert(END, file_cont)
    tf.close()
    canvas2 = Canvas(ws, width =200, height =-2) 
    canvas2.pack(fill=BOTH,expand=1)    

    btn=Button(ws,text="EXIT",height=1,width=15,bg="#cf0000",fg="white",font=('Courier',11,'bold'),command=lambda:ws.destroy())
    btn.pack( side=BOTTOM,pady=(10,8))

    canvas2 = Canvas(ws, width =200, height =-2) 
    canvas2.pack(fill=BOTH,expand=1,side=BOTTOM)  

    btn=Button(ws,text="Visualise",height=1,width=12,bg="#233e8b",fg="white",font=('Courier',11,'bold'),command= lambda:visGcode(fileO))
    btn.pack( side=LEFT,pady=10,padx=10)
    
    lbl2=Label(ws,text="Slower(x)")
    lbl2.pack(anchor = W,side=LEFT,padx=5 )
    lbl2.config(background="#4aa96c",font=('Arial',13),foreground='white')
    T2 = Text(ws, height =1, width =4,foreground='red',font=('Arial',9))
    T2.pack(anchor = W,side=LEFT,padx=2 ) 

    lbl3=Label(ws,text="Zoom(x)")
    lbl3.pack(anchor = W,side=LEFT,padx=5 )
    lbl3.config(background="#4aa96c",font=('Arial',13),foreground='white')
    T3 = Text(ws, height =1, width =4,foreground='red',font=('Arial',9))
    T3.pack(anchor = W,side=LEFT,padx=2 ) 

    btn=Button(ws,text="COM-PORT",bg="#233e8b",fg="white",height=1,font=('Courier',11,'bold'),width=12,command=lambda:CommSell(dim,fileO))
    btn.pack( side=RIGHT,padx=10)
    
      
    ws.wm_protocol("WM_DELETE_WINDOW", ws.destroy) 
    addDef()
    ws.mainloop()


# fileReader("dir_Gcode/",40)