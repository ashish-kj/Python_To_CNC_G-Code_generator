from tkinter import *
import time
from tkinter.ttk import *
from tkinter import filedialog
from PIL import ImageTk, Image,ImageOps
import os
import cv2
import numpy as np
import Edittor
from tkinter import filedialog as fd
import serial
import serial.tools.list_ports
import time



fName=None
count=0
rep=False
xx=0
yy=0
found=False
port=None

def addDef():
     T.delete("1.0","end")
     T.insert(END, "40")
     T2.delete("1.0","end")
     T2.insert(END, "5")
     T3.delete("1.0","end")
     T3.insert(END, "5")

def visualise1(arr,k):
      
     cv2.line(imm,(int(arr[0]*k),int((arr[1]*k))),(int(arr[0]*k),int(arr[1]*k)), (255, 255, 255), 1)
     data = Image.fromarray(imm)
     img2= ImageTk.PhotoImage(data)
     panel.configure(image=img2)
     panel.image = img2
     cv2.waitKey(1)
     root.update()



def run(acc,linSpace,dim):
     
     global imm,count
     RRsize()
     im = cv2.imread('dir_in/savedImage1000x.jpg',0)
     h,w=im.shape
     tp=max(h,w)
     k=1
     prg=h//100
     if(h>500): k=500/h
     
     imm=np.zeros((500,500,3),np.uint8) 
     flag=False
     up=True
     
     file = open(fName+"/output.gcode", "w")
     file.write("M300 S50.00 (pen Up)\n")
     file.write("G1 X0.00 Y0.00 F3500.00 (Start from home)\n")

    

     for i in range(0,h,acc):
          for j in range(0,w,linSpace):
   
               if im[i][j]<127: 
                    visualise1([j,i],k)
                    x1 = str(round(j*(dim/tp),2))
                    y1 = str(round(i*(dim/tp),2))

                    file.write("G1 "+"X" + x1 + " Y" + y1 + "\n")
                    label4.config(text =f"G1  X{x1}  Y{y1}")
                    root.update_idletasks()
                    root.update()

                    strs="G1 "+"X" + x1 + " Y" + y1 + "\n"
                    if found and CheckVar1.get(): 
                         port.write(strs.encode())
                         time.sleep(.1)  
                         msg=port.readline().decode('utf-8')
                         print(msg)

                    file.write("M300 S30.00 (pen down)\n")
                    if found and CheckVar1.get(): 
                         port.write("M300 S30.00 (pen down)\n".encode())
                         time.sleep(.1)  
                         msg=port.readline().decode('utf-8')
                         print(msg)

                    file.write("M300 S50.00 (pen Up)\n")
                    if found and CheckVar1.get(): 
                         port.write("M300 S50.00 (pen Up)\n".encode())
                         time.sleep(.1)  
                         msg=port.readline().decode('utf-8')
                         print(msg)   

          if((i//prg)-count >=1):
               count+=1
               progress['value'] =count
               root.update_idletasks()
     
     if(count!=100):
          progress['value']=100
          root.update_idletasks()

     cv2.destroyAllWindows()
     file.write("M18\nEnd ----->\n")
     file.close()

     
def RRsize():

    img = cv2.imread('dir_in/savedImage1000x.jpg')
    h,w,ch= img.shape  
    d=max(h,w)  
    color = (255,255,255)
    result = np.full((d,d,ch), color, dtype=np.uint8)
    xx = (d-w)//2
    yy = (d-h)//2
    result[yy:yy+h, xx:xx+w] = img
    cv2.imwrite('dir_in/savedImage1000x.jpg', result)

def nextt(d):
     root.destroy()
     Edittor.fileReader(fName,d)

def select_file():

    global fName  
    fName=fd.askdirectory()
    label.config(text = str(fName)) 
    label.config(background="#4aa96c",font=('Arial',13),foreground='white')  

def convertFinal():

     global rep,count
     count=0

     if(fName==None or fName==""):
          label.config(text ="Choose the output Directory!")
          label.config(background="#4aa96c",font=('Arial',13),foreground='black')   
          return     

     d=int(T.get(1.0, "end-1c"))
     linespace=int(T2.get(1.0, "end-1c"))
     acc=int(T3.get(1.0, "end-1c"))

     if(linespace==0 or acc==0):
          label.config(text ="Fileds should be Greater than the NULL Value !")
          label.config(background="#4aa96c",font=('Arial',13),foreground='black')   
          return
     else:
          label.config(text = str(fName)) 
          label.config(background="#4aa96c",font=('Arial',13),foreground='white')        


     run(acc,linespace,d)

     if rep==False:
          open_btt = Button(root,text='Next',width=16,command=lambda:nextt(d))
          open_btt.pack( anchor = W,padx=10,side=RIGHT)
          rep=True

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

    if found==False:
        for tempport in portlist:
            if tempport[0].startswith(val):
                try : 
                    port=serial.Serial(tempport[0])
                    port.baudrate =int(Tb.get(1.0, "end-1c"))
                    # port.write("M18\n".encode())
                    found=True  
                except:
                    found=False
    
    # print(found)
    while(True and found==False):
        progress3['value'] =count
        count=count-1
        newwin.update_idletasks()
        newwin.update()
        time.sleep(0.005)
        if(count==-1):
            lcom.config(text ="Connection Failed")
            lcom.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='black')
            break           

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

    if(found==True): 
        # time.sleep(5)
        port.baudrate = 4800
        # port.write("G1 X0. Y0.\n".encode())
        port.write("M18\n".encode())
        # port.close()

def cUP():

    if found==False:
          lcom.config(text ="Connection not Found!")
          lcom.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='black')
          return

    global xx,yy
    k=int(T.get(1.0, "end-1c"))
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
    k=int(T.get(1.0, "end-1c"))
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
    k=int(T.get(1.0, "end-1c"))
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
    k=int(T.get(1.0, "end-1c"))
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

def ComSel():
    
    global progress3,newwin,Tb,lcom

    if(CheckVar1.get()==0):
        newwin.destroy()
        return

    newwin = Toplevel(root)
    newwin.title('COM-PORT Connection')
    newwin['bg']='#4aa96c'
    newwin.resizable(0, 0)

   

    Label(newwin,text="COM-PORT Connection",background="#4aa96c",font=('Arial',14,"bold"),foreground='White',width=20).pack(pady=3)
    canvas2 = Canvas(newwin, height =-1) 
    canvas2.pack(fill=BOTH,expand=1,pady=2)
    options = ["SELECT PORT","Tuesday"]
    portlist = list(serial.tools.list_ports.comports())
 
    for tempport in portlist:
        options.append(str(tempport[0]))

    button3=Button(newwin,text='Save & Exit',width=15,command=lambda:newwin.destroy())
    button3.pack(pady=10,padx=10,side=BOTTOM)  
    
    canvas2 = Canvas(newwin, height =-4) 
    canvas2.pack(fill=BOTH,expand=1,side=BOTTOM)
    frame_1 = Frame(newwin, width=250, height=70)
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
    canvas2 = Canvas(newwin, height =-4) 
    canvas2.pack(fill=BOTH,expand=1,side=BOTTOM)

    open_button =Button(newwin,text='Connect',width=25,command=lambda:toSerial(clicked.get()))
    open_button.pack(pady=3,padx=10,side=BOTTOM)  
    
    lcom =Label(newwin,text="")
    lcom.pack(side=BOTTOM,padx=8,pady=5)
    lcom.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='white')
    
    

    canvas2 = Canvas(newwin, height =-4) 
    canvas2.pack(fill=BOTH,expand=1,side=BOTTOM)
    progress3= Progressbar(newwin, orient = HORIZONTAL,length =400, mode = 'determinate')
    progress3.pack(pady = 2,side=BOTTOM)  
    canvas2 = Canvas(newwin, height =-4) 
    canvas2.pack(fill=BOTH,expand=1,side=BOTTOM)
  
    clicked = StringVar()
    clicked.set( "SELECT PORT" )
    drop = OptionMenu( newwin , clicked , *options ).pack(side=LEFT,padx=10,pady=15)
   
   
    Tb = Text(newwin, height =1, width =9,foreground='red',font=('Arial',9))
    Tb.pack(anchor = E,side=RIGHT,padx=10,pady=1)
    Tb.delete("1.0","end")
    Tb.insert(END, "9600")

    lbl=Label(newwin,text="Baudrate:")
    lbl.pack(anchor =E,side=RIGHT,padx=5,pady=1)
    lbl.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='white')

   
    if(found==True):
        progress3['value'] =100
        lcom.config(text ="Connection ESTD !")
        lcom.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='White')
        clicked.set(gval)
     
    newwin.mainloop()

def sel():

   if(var.get()==1):
     immmg = Image.open('dir_in/resize.jpg')
     immmgI = ImageOps.invert(immmg)
     immmgI.save('dir_in/resize.jpg', quality=95)
     
     immmg2 = Image.open('dir_in/savedImage1000x.jpg')
     immmgI2 = ImageOps.invert(immmg2)
     immmgI2.save('dir_in/savedImage1000x.jpg', quality=95)

     img2= ImageTk.PhotoImage(Image.open('dir_in/resize.jpg'))
     panel.configure(image=img2)
     panel.image = img2 
     root.update()     


def bandline2():
     
     global root,progress,var,CheckVar1,label,T,T2,T3,panel,img,label4

     root = Tk()
     root.title('Setup.ex') 
     root['bg']='#4aa96c'
     root.resizable(False, False)
     # root.geometry('1000x850') 
 
     Label(root, text ="DOT Compilation", font=('Arial',20,'bold'),foreground="White",background="#4aa96c").pack()
     canvas2 = Canvas(root, width =200, height =-1) 
     canvas2.pack(fill=BOTH,expand=1,pady=2)
     # newWindow.wm_protocol("WM_DELETE_WINDOW", root.destroy)  
     img = ImageTk.PhotoImage(Image.open(f'dir_in/resize.jpg'))
     panel = Label(root, image = img)
     panel.pack(anchor= CENTER,pady=22)
     # //progress bar code


     # label =Label(root,text="")
     # label.pack(anchor = W,padx=3)
     # label.config(background="#4aa96c",font=('Arial',13),foreground='white')
     
     #  ///////////////////////////////////////////////////////////////////
     Style().configure('W.TFrame',background="#4aa96c",font=('Arial',13), foreground='white')
     frame_1 = Frame(root, style='W.TFrame',width=1100, height=70)
     frame_1.pack(fill=BOTH, expand=1)

     label4 =Label(frame_1,text="",width=20)
     label4.pack(side=RIGHT)
     label4.config(background="#4aa96c",font=('Arial',14,"bold"),foreground='White')

     label =Label(frame_1,text="")
     label.pack(side=LEFT)
     label.config(background="#4aa96c",font=('Arial',13),foreground='white')
    # /////////////////////////////////////////////////////////////////////

     canvas2 = Canvas(root, width =200, height =-4) 
     canvas2.pack(fill=BOTH,expand=1)
     progress = Progressbar(root, orient = HORIZONTAL,length =1000, mode = 'determinate')
     progress.pack(pady =2)
     canvas2 = Canvas(root, width =200, height =-4) 
     canvas2.pack(fill=BOTH,expand=1)
     # adding the radio bnuttons 
     
     CheckVar1 = IntVar()
     Style().configure('TCheckbutton',background="#4aa96c",font=('Arial',13), foreground='white')
     C1 = Checkbutton(root,style='TCheckbutton', text = "COM-Live", variable = CheckVar1,onvalue = 1, offvalue = 0,command=ComSel)
     C1.pack( anchor = W,side=LEFT,padx=4,pady=3)

     var = IntVar()
     Style().configure('Wild.TRadiobutton',background="#4aa96c",font=('Arial',13), foreground='white') 
     R1 = Radiobutton(root, text="Invert",style='Wild.TRadiobutton',variable=var, value=1,command=sel)
     R1.pack( anchor = W,side=LEFT,padx=10 )

    
     lbl=Label(root,text="Dimension(mm):")
     lbl.pack(anchor = W,side=LEFT,padx=5 )
     lbl.config(background="#4aa96c",font=('Arial',13),foreground='white')
     T = Text(root, height =1, width =7,foreground='red',font=('Arial',9))
     T.pack(anchor = W,side=LEFT,padx=2 )

     lbl2=Label(root,text="X-Space(px):")
     lbl2.pack(anchor = W,side=LEFT,padx=5 )
     lbl2.config(background="#4aa96c",font=('Arial',13),foreground='white')
     T2 = Text(root, height =1, width =4,foreground='red',font=('Arial',9))
     T2.pack(anchor = W,side=LEFT,padx=2 )

     lbl3=Label(root,text="Y-Space(px):")
     lbl3.pack(anchor = W,side=LEFT,padx=5 )
     lbl3.config(background="#4aa96c",font=('Arial',13),foreground='white')
     T3 = Text(root, height =1, width =4,foreground='red',font=('Arial',9))
     T3.pack(anchor = W,side=LEFT,padx=2 )
       
     open_button =Button(root,text='Proceed',width=20,command=convertFinal)
     open_button.pack(pady=10,side=RIGHT,padx=10)

     open_btn = Button(root,text='Output Location',width=16,command=select_file)
     open_btn.pack( anchor = W,padx=10,side=RIGHT)

     root.wm_protocol("WM_DELETE_WINDOW", root.destroy) 
     addDef()
     root.mainloop()

# bandline2()
