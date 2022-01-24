import os 
import cv2
import math as mt
import numpy as np
import cv2
from tkinter import *
import tkinter
from PIL import Image, ImageDraw, ImageEnhance
from itertools import product
import math as mt

tp=400  
mode=2
SMOOTHERR =1	
done = set()        
direc = 0    
up=True
file=None
count=0


def draw(arr):
    
     
     cv2.line(imm,(int(arr[1][0]*(500/tp)),int((arr[1][1]*(500/tp)))),(int(arr[0][0]*(500/tp)),int(arr[0][1]*(500/tp))), (57, 255, 20), 1)
     data = Image.fromarray(imm)
     img2= ImageTk.PhotoImage(data)
     panel.configure(image=img2)
     panel.image = img2
     cv2.waitKey(1)
     root.update()

def setValue(val,m,dd,fileO):

     global tp,mode,file,d
     tp=int(val)
     mode=m
     d=dd
     file = open(fileO+'/output.gcode', "a")

def reInitialise():
     done=set()
     direc=0

def clearing():

     global file
     file.write("M18 (End) ") 
     file.close()


def dir(ci,cj,row,col):
     pass
     if ci%2==0 :
          if cj==col-1:
               return "DOWN"
          else:
               return "RIGHT"
     if ci%2!=0:
          if (col-cj-1)==0:
               return "DOWN"
          else:
               return "LEFT"

def gridGcode():
    
     global count,label3
     img = Image.open('dir_in/result.jpg')
     w, h= img.size
     row=h//tp    
     col=w//tp
     k=100/(row*col)

     for i  in range(0,row):
          for j in range(0,col):

               if(i%2==0): 
                   fname=f"dir_out/{i}x{j}.jpg" 
                   fname2=f"{i}x{j}.jpg"
               else: 
                   fname=f"dir_out/{i}x{col-j-1}.jpg"
                   fname2=f"{col-j-1}.jpg"

            #    print(fname)
            #    print(dir(i,j,row,col))
               label3.config(text =f"Direction-{dir(i,j,row,col)}   Filename-({fname2})")
               progress['value'] =count
               count=count+k
               root.update_idletasks() 

               imToPaths(fname)

               file.write("G1 X0.00 Y0.00 F3500.00 (go home)\n")
               if found and CheckVar1.get(): 
                    port.write("G1 X0.00 Y0.00 F3500.00 (go home)\n".encode())
                    time.sleep(.1)
                    msg=port.readline().decode('utf-8')
                    print(msg)
      
            
               file.write(f"{dir(i,j,row,col)}-Direction TO MOVEEEEE!!!!>>>>>>\n")
               if found and CheckVar1.get(): 
                    port.write(f"{dir(i,j,row,col)}-Direction TO MOVEEEEE!!!!>>>>>>\n".encode())
                    time.sleep(.1)
                    msg=port.readline().decode('utf-8')
                    print(msg)

               reInitialise()
                    

def split():

     img = Image.open('dir_in/result.jpg')
     w, h = img.size
     grid = list(product(range(0, h-h%tp, tp), range(0, w-w%tp, tp)))
     for i, j in grid:
          box = (j, i, j+tp, i+tp)
          out =f'dir_out/{int(i/tp)}x{int(j/tp)}.jpg'
          img.crop(box).save(out)

def Rsize():

     img = cv2.imread('dir_in/savedImage1000x.jpg')
     h,w,ch= img.shape
     ww =w + tp - w%tp
     hh = h + tp - h%tp
     color = (255,255,255)
     result = np.full((hh,ww,ch), color, dtype=np.uint8)
     xx = (ww - w) // 2
     yy = (hh - h) // 2

     result[yy:yy+h, xx:xx+w] = img
     cv2.imwrite(f"dir_in/result.jpg", result)

def RRsize(filename):
    
    global tp
    img = cv2.imread(filename)
    h,w,ch= img.shape          
    color = (255,255,255)
    result = np.full((tp,tp,ch), color, dtype=np.uint8)
    xx = (tp-w)//2
    yy = (tp-h)//2
    result[yy:yy+h, xx:xx+w] = img
    cv2.imwrite("dir_in/RRsize.jpg", result)
    if(var.get()==44):

        tp=int(d*3.7795275591)
        im = Image.open("dir_in/RRsize.jpg")
        resized_im = im.resize((tp,tp))
        resized_im.save("dir_in/RRsize.jpg")

    if(var.get()==33):

        tp=int(2*d*3.7795275591)
        im = Image.open("dir_in/RRsize.jpg")
        resized_im = im.resize((tp,tp))
        resized_im.save("dir_in/RRsize.jpg")
   
    if(var.get()==22):
        im = Image.open("dir_in/RRsize.jpg")
        tp=int(round(im.size[0]*0.5))
        resized_im = im.resize((round(im.size[0]*0.5), round(im.size[1]*0.5)))
        resized_im.save("dir_in/RRsize.jpg")
 

    # im = Image.open("dir_in/RRsize.jpg")
    # resized_im = im.resize((round(im.size[0]*0.5), round(im.size[1]*0.5)))

def initRaster(filename):
    
    if(mode==1):
        RRsize(filename)
        im = Image.open('dir_in/RRsize.jpg')
        return im
    if(mode==2):
        im = Image.open(filename)
        return im
    
def readFromRaster(filename):

    global done,file

    im = initRaster(filename)
    point = nextShape(im)
    nextpoint = (0, 0)

    while point != (-1, -1):
        start = point
        shape=[]
        shape.append(point)
        while nextpoint != start:
            nextpoint = nextPixelInShape(im, point)
            point = nextpoint
            done.add(point)
            shape.append(point)

        smoothShape = smoothRasterCoords(shape)
        if smoothShape[-1] != smoothShape[0]:
            smoothShape.append(smoothShape[0])
        
        toTextFile2(smoothShape)
        print(smoothShape,'\n------------------------------------>')
        point = nextShape(im)

    print("Done gcode")

def toTextFile2( shape):
    
    global up,count,buffer
    up = True

    for i in range(len(shape)):

        xstr = str(round(shape[i][0]*(d/tp),2))
        ystr = str(round(shape[i][1]*(d/tp),2))
            
        file.write("G1 "+"X" + xstr + " Y" + ystr + "\n")
        label4.config(text =f"G1  X{xstr}  Y{ystr}")
        root.update_idletasks()
        root.update()

        straa="G1 "+"X" + str(xstr) + " Y" + str (ystr) + "\n"
        if found and CheckVar1.get(): 
            port.write(straa.encode())
            time.sleep(.05)  
            msg=port.readline().decode('utf-8')
            print(msg)
            
            if(mode==1):
                buffer.append([shape[i][0],shape[i][1]])
                if(len(buffer)==2):
                    draw(buffer)
                    buffer.pop(0)

        if up == True and CheckVar1.get():
            file.write("M300 S30.00 (pen down)\n")
            if found : 
                port.write("M300 S30.00 (pen down)\n".encode())
                time.sleep(.1)
                msg=port.readline().decode('utf-8')
                print(msg)
            up = False   

    file.write("M300 S50.00 (pen up)\n")
    if found and CheckVar1.get(): 
        port.write("M300 S50.00 (pen up)\n".encode())
        time.sleep(.1)
        msg=port.readline().decode('utf-8')
        print(msg)

        if(mode==1):
            if(len(buffer)==1):
                    buffer.append([buffer[0][0],buffer[0][1]])
                    draw(buffer)
            buffer=[]

    up = True

    if(mode==1 and count<=86):
        progress['value'] =count
        count=count+1
        root.update_idletasks()


def imToPaths(filename):
   
    if filename.endswith((".jpg", ".jpeg", ".png", ".bmp")):
        readFromRaster(filename)
  
def smoothRasterCoords(coords):

    newCoords = []
    if len(coords) <= 2:
        newCoords = coords

    i = 0
    while i < len(coords) - 2:
        j = len(coords) - 1
        while j > i + 1:
                midpoints = coords[i + 1:j]
                try:
                    m = (coords[j][1] - coords[i][1])/(coords[j][0] - coords[i][0])
                    b = coords[i][1] - m * coords[i][0]
                    canDel = True
                    for point in midpoints:
                        if abs((m * point[0] - point[1] + b)/((m ** 2 + 1) ** 0.5)) >= SMOOTHERR:
                            canDel = False
                            break

                    if canDel == True:
                        newCoords.append(coords[i])
                        newCoords.append(coords[j])
                        i = j

                except ZeroDivisionError:

                    canDel = True
                    for point in midpoints:
                        if abs(coords[i][0] - point[0]) >= SMOOTHERR:
                            canDel = False
                            break
                    if canDel == True:
                        newCoords.append(coords[i])
                        newCoords.append(coords[j])
                        i = j
                j -= 1
        i += 1

    if len(newCoords) == 0:
        return coords
        
    return newCoords

def isOnEdge(im, px):

    hues = []
    try: hues.append(sum(im.getpixel((px[0] - 1, px[1]))))
    except IndexError: hues.append(sum((255, 255, 255)))
    
    try: hues.append(sum(im.getpixel((px[0], px[1] - 1))))
    except IndexError: hues.append(sum((255, 255, 255)))
    
    try: hues.append(sum(im.getpixel((px[0] + 1, px[1]))))
    except IndexError: hues.append(sum((255, 255, 255)))
    
    try: hues.append(sum(im.getpixel((px[0], px[1] + 1))))
    except IndexError: hues.append(sum((255, 255, 255)))    

    if (max(hues) > sum((127, 127, 127))):
        return True
    else:
        return False

def nextPixelInShape(im, px):
    global direc, done
    while True:
        pixels = im.load()
        try: pixel = sum(im.getpixel((px[0], px[1])))
        except IndexError: pixel = sum((255, 255, 255))
        if pixel < sum((127, 127, 127)):
            direc = (direc - 1) % 4
        else:
            direc = (direc + 1) % 4
        if direc == 0:
            x = px[0] + 1
            y = px[1]
        elif direc == 1:
            x = px[0]
            y = px[1] + 1
        elif direc == 2:
            x = px[0] - 1
            y = px[1]
        elif direc == 3:
            x = px[0]
            y = px[1] - 1
        try: pixel = sum(im.getpixel((x, y)))
        except IndexError: pixel = sum((255, 255, 255))
        if pixel < sum((127, 127, 127)):
            if (x, y) not in done:
                done.add((x, y))
            return (x, y)
        else:
            px=(x, y)

def nextShape(im):
    global done

    for x in range(tp):
        for y in range(tp):
            if sum(im.getpixel((x, y))) < sum((127, 127, 127)) and\
               isOnEdge(im, (x, y)) and not (x, y) in done:
                done.add((x, y))
                return(x, y)
    return (-1, -1)

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
from tkinter import *
from tkinter import ttk
import time
from tkinter.ttk import *
from tkinter import filedialog
from PIL import ImageTk, Image,ImageOps
import os
import Edittor
from tkinter import filedialog as fd
import serial
import serial.tools.list_ports
import time


fName=None
count=1
found=False
port=None
xx=0.00
yy=0.00

def update():
     global count
     progress['value'] =count
     root.update_idletasks()
     time.sleep(.01)
     count=count+1

def addDef():
     T.delete("1.0","end")
     T.insert(END, "40")

def select_file():

    global fName  
    fName=fd.askdirectory()
    label2.config(text = str(fName))
    label2.config(background="#4aa96c",font=('Arial',13),foreground='white')  

def convertFinal():


     if fName==None or fName=="" :
         label2.config(text ="Choose the output Directory!")
         label2.config(background="#4aa96c",font=('Arial',13),foreground='black')
         return

     if m==1 and var.get()==0 :
         label.config(text ="Choose Any Mode!")
         label.config(background="#4aa96c",font=('Arial',13),foreground='black')
         return

     d=int(T.get(1.0, "end-1c"))

     GcodeGen(fName,d,m) 
     root.destroy()
     Edittor.fileReader(fName,d)

def sel():

   if(var.get()==11):
     label.config(text = "Slow Mode is Selected")
     label.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='white') 
   elif(var.get()==22):
     label.config(text="Medium Mode is Selected")
     label.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='white') 
   elif (var.get()==33):
     label.config(text="Fast Mode is Selected")
     label.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='white') 
   elif (var.get()==44):
     label.config(text="Super-Fast Mode is Selected")
     label.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='white') 


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

def Invert():

    print(CheckVar2.get())

    if(CheckVar2.get()==1 or CheckVar2.get()==0):
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


def band(mode):

     global root,progress,var,CheckVar1,CheckVar2,label,T,m,label2,T2,label3,label4,C1,panel,buffer,imm
     m=mode
     buffer=[]
     imm=np.zeros((600,600,3),np.uint8) 

     root = Tk()
     root.title('Setup.ex') 
     root['bg']='#4aa96c'
     root.resizable(False, False)
     if mode==1:
         text="Raster Compilation"
     elif mode==2:
         text="Matrix Compilation"
 
     Label(root, text =text, font=('Arial',20,'bold'),foreground="White",background="#4aa96c").pack()
     canvas2 = Canvas(root, width =200, height =-1) 
     canvas2.pack(fill=BOTH,expand=1,pady=2)
     # newWindow.wm_protocol("WM_DELETE_WINDOW", root.destroy)  
     img = ImageTk.PhotoImage(Image.open(f'dir_in/resize.jpg'))
     panel = Label(root, image = img)
     panel.pack(anchor= CENTER,pady=10)
     

    #  ///////////////////////////////////////////////////////////////////
     Style().configure('W.TFrame',background="#4aa96c",font=('Arial',13), foreground='white')
     frame_2 = Frame(root,style='W.TFrame',width=1100, height=70)
     frame_2.pack(fill=BOTH, expand=1)

     label4 =Label(frame_2,text="",width=20)
     label4.pack(side=RIGHT)
     label4.config(background="#4aa96c",font=('Arial',14,"bold"),foreground='White')

     label2 =Label(frame_2,text="")
     label2.pack(side=LEFT)
     label2.config(background="#4aa96c",font=('Arial',13),foreground='white')
    # /////////////////////////////////////////////////////////////////////

     
     
     canvas2 = Canvas(root, width =200, height =-4) 
     canvas2.pack(fill=BOTH,expand=1)
     progress = Progressbar(root, orient = HORIZONTAL,length =1100, mode = 'determinate')
     progress.pack(pady = 2)
     canvas2 = Canvas(root, width =200, height =-4) 
     canvas2.pack(fill=BOTH,expand=1)
     # adding the radio bnuttons 
     var = IntVar()
     open_btn = Button(root,text='Output Location',width=16,command=select_file)
     open_btn.pack( anchor = W,side=LEFT,padx=10)
     Style().configure('Wild.TRadiobutton',background="#4aa96c",font=('Arial',13), foreground='white')
     Style().configure('TCheckbutton',background="#4aa96c",font=('Arial',13), foreground='white')
     
     CheckVar1 = IntVar()
     C1 = Checkbutton(root,style='TCheckbutton', text = "COM-Live", variable = CheckVar1,onvalue = 1, offvalue = 0,command=ComSel)
     C1.pack( anchor = W,side=LEFT,padx=4,pady=3)
     CheckVar2 = IntVar()
     C2 = Checkbutton(root,style='TCheckbutton', text = "Invert", variable = CheckVar2,onvalue = 1, offvalue = 0,command=Invert)
     C2.pack( anchor = W,side=LEFT,padx=4,pady=3)

     Label(root,text="|",background="#4aa96c",font=('Arial',18),foreground='white').pack(anchor = W,side=LEFT,padx=5 )

     if(mode==1):
        R1 = Radiobutton(root, text="S",style='Wild.TRadiobutton',variable=var, value=11,command=sel)
        R1.pack( anchor = W,side=LEFT,padx=4,pady=3)
        R2 = Radiobutton(root, text="M",style='Wild.TRadiobutton',variable=var, value=22,command=sel)
        R2.pack( anchor = W,side=LEFT,padx=4,pady=3 )
        R3 = Radiobutton(root, text="F",style='Wild.TRadiobutton',variable=var, value=33,command=sel)
        R3.pack( anchor = W,side=LEFT,padx=4,pady=3 )
        R4 = Radiobutton(root, text=" SF",style='Wild.TRadiobutton',variable=var, value=44,command=sel)
        R4.pack( anchor = W,side=LEFT,padx=4,pady=3 )
        Label(root,text="|",background="#4aa96c",font=('Arial',18),foreground='white').pack(anchor = W,side=LEFT,padx=5 )


    
     lbl=Label(root,text="Dimension:")
     lbl.pack(anchor = W,side=LEFT,padx=5 )
     lbl.config(background="#4aa96c",font=('Arial',13),foreground='white')
     T = Text(root, height =1, width =7,foreground='red',font=('Arial',9))
     T.pack(anchor = W,side=LEFT,padx=2 )

     if(mode==1):
        label =Label(root,text="")
        label.pack(anchor = W,side=LEFT,padx=10 )
        label.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='white')
     if(mode==2):
        label3 =Label(root,text="Current Direction-Filename")
        label3.pack(anchor = W,side=LEFT,padx=10 )
        label3.config(background="#4aa96c",font=('Arial',13,"bold"),foreground='white')

   
     
     open_button =Button(root,text='Proceed',width=20,command=convertFinal)
     open_button.pack(pady=10,side=RIGHT,padx=10)

     root.wm_protocol("WM_DELETE_WINDOW", root.destroy) 
     addDef()
     root.mainloop()
    

# band(2)



# ///////////////////////////////////////////////////////////////////////////////////////////////////////////////
def GcodeGen(fileO,d,mode):
     
    #  print('sdfsdfdsfsdf',fileO)
     if(mode==2):
     # for matrix method
    
          setValue(mt.floor(d*3.7795275591),mode,d,fileO)
          Rsize()
          split()
          gridGcode()
          clearing()

     elif(mode==1):
     # for single method
          global count
          while(True):
            progress['value'] =count
            root.update_idletasks()
            time.sleep(.01)
            count=count+1
            if (count>=25):
                break   

          img = Image.open('dir_in/savedImage1000x.jpg')
          w, h = img.size
          setValue(max(w,h),mode,d,fileO)
          imToPaths('dir_in/savedImage1000x.jpg')
          clearing()
           
          while(True):
            progress['value'] =count
            root.update_idletasks()
            time.sleep(.01)
            count=count+1
            if (count>=100):
                break   

            
     
     print("Done gcode>>>>>>>>")


# d=40
# GcodeGen("",d,2)
# band(2)