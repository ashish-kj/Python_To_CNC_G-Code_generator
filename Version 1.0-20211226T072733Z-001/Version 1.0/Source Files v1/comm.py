from tkinter import *
import time
from tkinter.ttk import *
from tkinter import filedialog
from PIL import ImageTk, Image,ImageOps
import os
import cv2
import numpy as np
from tkinter import filedialog as fd
import serial
import serial.tools.list_ports
import time

xx=0
yy=0
found=False
port=None

3
def draw(arr):
     
     cv2.line(imm,(arr[1][0],arr[1][1]),(arr[0][0], arr[0][1]), (57, 255, 20), 1)
     data = Image.fromarray(imm)
     img2= ImageTk.PhotoImage(data)
     panel.configure(image=img2)
     panel.image = img2
     newwin.update()

def toSerial(val):

    if(val=="SELECT PORT"):
        lcom.config(text ="Select the Port!")
        lcom.config(background="#4aa96c",font=('Arial',13),foreground='black')
        return

    global found,port,gval
    gval=val
    portlist = list(serial.tools.list_ports.comports())

    count=1
    while(True):
        progress3['value'] =count
        count=count+1
        newwin.update_idletasks()
        newwin.update()
        time.sleep(0.005)
        if(count==45):break

    for tempport in portlist:
        if tempport[0].startswith(val):
            try : 
                port=serial.Serial(tempport[0])
                port.baudrate =int(Tb.get(1.0, "end-1c"))
                # port.write("M18\n".encode())
                found=True  
            except:
                 found=False

    while(True and found==False):
        progress3['value'] =count
        count=count-1
        newwin.update_idletasks()
        newwin.update()
        time.sleep(0.005)
        if(count==-1):
            lcom.config(text ="Connection Failed")
            lcom.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='black')
            return           

    while(True and found==True):
        progress3['value'] =count
        count=count+1
        newwin.update_idletasks()
        
        newwin.update()
        time.sleep(0.005)
        if(count==100):
            lcom.config(text ="Connection ESTD !")
            lcom.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='White')
            break 
    
    print(" Communication Established.......")
 # ////////////////////////////////////////////////////////////////////////////////////////connedted

def sendGcode(fileO,dim):
    
    if found==False:
        lcom.config(text ="Connection not Found!")
        lcom.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='black')
        return
        
    global imm
    imm=np.zeros((400,400,3),np.uint8) 

    file = open(fileO+"/output.gcode", "r")
    size=len(file.readlines())
    size=size//100
    file.close()
    file = open(fileO+"/output.gcode", "r")
    count2=1

    x,y=0,0
    buffer=[]
    Z=400/dim
   
    while True:
        
        progress3.start(10)  

        line = file.readline()
        if line[0:3]=="M18" or line==False: break

        port.write(line.encode())
        msg=port.readline().decode('utf-8')
        print(msg)
    
        # /////code for visualising the Gcode
        if(line[0]=='G'):
        
               indx=line.find('X')
               indy=line.find('Y')
               x=int(float(line[indx+1:indy-1])*Z)
               y=int(float(line[indy+1:indy+5])*Z)
               buffer.append([x,y])
               if(len(buffer)==2):
                    draw(buffer)
                    buffer.pop(0)
    
        if(line[5:8]=="S50" and line[0]=="M"):
               up=True
               if(len(buffer)==1):
                    buffer.append([buffer[0][0],buffer[0][1]])
                    draw(buffer)
               buffer=[]

        if(count2==size):
            progress4['value']+=1
            count2=0

        count2=count2+1
        newwin.update_idletasks()
        newwin.update() 

    progress3.stop()   
    file.close()
    port.close()
    print("exit here") 

def cUP():
    
    if found==False:
        lcom.config(text ="Connection not Found!")
        lcom.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='black')
        return


    global xx,yy
    xx=xx
    yy=yy+k
    if yy>=k: yy=k
    if yy<0: yy=0.00
    if xx>=k: xx=k
    if xx<0: xx=0.00
    port.write(f"G1 X{xx} Y{yy}\n".encode())

def cDOWN():
    
    if found==False:
        lcom.config(text ="Connection not Found!")
        lcom.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='black')
        return

    global xx,yy
    xx=xx
    yy=yy-k
    if yy>=k: yy=k
    if yy<0: yy=0.00
    if xx>=k: xx=k
    if xx<0: xx=0.00
    port.write(f"G1 X{xx} Y{yy}\n".encode())

def cLEFT():
    
    if found==False:
        lcom.config(text ="Connection not Found!")
        lcom.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='black')
        return


    global xx,yy
    xx=xx-k
    yy=yy
    if yy>=k: yy=k
    if yy<0: yy=0.00
    if xx>=k: xx=k
    if xx<0: xx=0.00
    port.write(f"G1 X{xx} Y{yy}\n".encode()) 

def cRIGHT():
    
    if found==False:
        lcom.config(text ="Connection not Found!")
        lcom.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='black')
        return

    global xx,yy
    xx=xx+k
    yy=yy
    if yy>=k: yy=k
    if yy<0: yy=0.00
    if xx>=k: xx=k
    if xx<0: xx=0.00
    port.write(f"G1 X{xx} Y{yy}\n".encode())

def cRESET():
    
    if found==False:
        lcom.config(text ="Connection not Found!")
        lcom.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='black')
        return
        
    # port.write("G1 X0.00 Y0.00\n".encode())
    port.write("G1 X40.00 Y0.00\n".encode())
    port.write("G1 X0.00 Y0.00\n".encode())
    port.write("G1 X0.00 Y40.00\n".encode())
    port.write("G1 X0.00 Y0.00\n".encode())

def ComSel(dim,fileO):
    
    global progress3,newwin,Tb,lcom,k,progress4,panel
    k=dim

    newwin = Tk()
    newwin.title('Setup.ex') 
    newwin['bg']='#4aa96c'
    newwin.resizable(False, False)

    options = ["SELECT PORT"]
    portlist = list(serial.tools.list_ports.comports())
    for tempport in portlist:
        options.append(str(tempport[0]))
    
    
    Label(newwin,text="COM-PORT Connection",background="#4aa96c",font=('Arial',14,"bold"),foreground='White',width=20).pack(pady=3)
    canvas2 = Canvas(newwin, height =-1) 
    canvas2.pack(fill=BOTH,expand=1)
    progress4= Progressbar(newwin, orient = HORIZONTAL,length =804, mode = 'determinate')
    progress4.pack(expand=1,side=BOTTOM) 

# //////////////////////////////////////////////////////////////////////////////////////////
    Style().configure('W.TFrame',background="#4aa96c",font=('Arial',13), foreground='white')
    frame_2 = Frame(newwin, style='W.TFrame',width=400, height=70)
    frame_2.pack(side=LEFT)


    frame_3 = Frame(newwin,width=400, height=70)
    frame_3.pack(side=RIGHT)
    img = ImageTk.PhotoImage(Image.open(f'dir_in/logo2.jpg'))
    panel = Label(frame_3, image = img)
    panel.pack(anchor= CENTER)

    # /////////////////////////////////////////////////////////////////////
    button3=Button(frame_2,text='Send Gcode',width=15,command=lambda:sendGcode(fileO,dim))
    button3.pack(pady=10,padx=10,side=BOTTOM)
        
    canvas2 = Canvas(frame_2, height =-4) 
    canvas2.pack(fill=BOTH,expand=1,side=BOTTOM)
    frame_1 = Frame(frame_2, width=250, height=70)
    frame_1.pack(pady=10,padx=10,side=BOTTOM)
    b1 = Button(frame_1, text="▲",command=cUP)
    b1.pack(side=TOP,pady=20)
    b2 = Button(frame_1, text="▼",command=cDOWN)
    b2.pack(side=BOTTOM,pady=20)
    b3 = Button(frame_1, text=">",command=cRIGHT)
    b3.pack(side=RIGHT,padx=20)
    b4 = Button(frame_1, text="<",command=cLEFT)
    b4.pack(side=LEFT,padx=20)
    b0 = Button(frame_1, text="Reset",command=cRESET)
    b0.pack(side=LEFT,padx=20)
    canvas2 = Canvas(frame_2, height =-4) 
    canvas2.pack(fill=BOTH,expand=1,side=BOTTOM)

    open_button =Button(frame_2,text='Connect',width=25,command=lambda:toSerial(clicked.get()))
    open_button.pack(pady=3,padx=10,side=BOTTOM)  
    
    lcom =Label(frame_2,text="")
    lcom.pack(side=BOTTOM,padx=8,pady=5)
    lcom.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='white')
    
    

    canvas2 = Canvas(frame_2, height =-4) 
    canvas2.pack(fill=BOTH,expand=1,side=BOTTOM)
    progress3= Progressbar(frame_2, orient = HORIZONTAL,length =400, mode = 'determinate')
    progress3.pack(pady = 2,side=BOTTOM)  
    canvas2 = Canvas(frame_2, height =-4) 
    canvas2.pack(fill=BOTH,expand=1,side=BOTTOM)
  
    clicked = StringVar()
    clicked.set( "SELECT PORT" )
    drop = OptionMenu( frame_2 , clicked , *options ).pack(side=LEFT,padx=10,pady=15)
   
   
    Tb = Text(frame_2, height =1, width =9,foreground='red',font=('Arial',9))
    Tb.pack(anchor = E,side=RIGHT,padx=10,pady=1)
    Tb.delete("1.0","end")
    Tb.insert(END, "9600")

    lbl=Label(frame_2,text="Baudrate:")
    lbl.pack(anchor =E,side=RIGHT,padx=5,pady=1)
    lbl.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='white')

   
    if(found==True):
        progress3['value'] =100
        lcom.config(text ="Connection ESTD !")
        lcom.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='White')
        clicked.set(gval)
     
    newwin.mainloop()


# ComSel(40,"dir_Gcode")    