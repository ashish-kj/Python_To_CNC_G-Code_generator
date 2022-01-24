import cv2
import os
import CBG
import dxf2G
import Edittor
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog as fd
import svg2G


# //function for choosing file from directory
def select_file():
    filetypes = (('All files', '*.*'),
                ('JPEG Image file', '*.jpg'),
                ('PNG Image file', '*.png'),
                ('DXF file', '*.dxf'),
                ('SVG file', '*.svg'))
    filename = fd.askopenfilename(title='Open a file',initialdir='/',filetypes=filetypes) 
    global fName  
    fName=filename
    T.delete("1.0","end")
    T.insert(INSERT,str(fName))
    T.configure(fg="White",font=('Arial',13,"bold"))
    T.tag_configure("center", justify='center')
    T.tag_add("center", "1.0", "end")


def sel():
    rasterGcode="Take Raster Images \n(*.jpg ,*.png) as \ninput and generate Gcode\nfile as Output along \nwith live visualisation.\nThere are modes for the \nquality of gcode to be \nGenerated. "
    MatrixFunction="Its a special function \nIt divides the image \ninto multiple rows and \ncols and append the gcode\nof each gridImage(ixj) \nsuccessively. I made\nThis Option for \nPersonal Use"
    HashPrinting="Take Raster Images \n(*.jpg ,*.png) as input \nand convert to HASHED \nimage and then produce \nGcode of the same.\nCom-Port connectivity is available along with live\nvisualisation."
    DotPrinting="Take Raster Images \n(*.jpg ,*.png) as input \nand convert to Dotted \nimage and then produce \nGcode of the same.\nCom-Port connectivity is available along with live\nvisualisation."
    svg="Takes *.svg image formate\nas input and Generate the\nGcode file"
    dxf="Takes *.dxf file formate\nas input and Generate the\nGcode file"
    vis="G-code Sender to send\nthe gcode file using \nCOM-PORT communication or\nBluetooth communication\nAlong with live \nVisualisation."

    val=var.get()

    if(val==1):
        txtarea.delete("1.0","end")
        txtarea.insert(END, rasterGcode)
    if(val==2):
        txtarea.delete("1.0","end")
        txtarea.insert(END, MatrixFunction)
    if(val==3):
        txtarea.delete("1.0","end")
        txtarea.insert(END, HashPrinting)
    if(val==4):
        txtarea.delete("1.0","end")
        txtarea.insert(END, DotPrinting)
    if(val==5):
        txtarea.delete("1.0","end")
        txtarea.insert(END, svg)
    if(val==6):
        txtarea.delete("1.0","end")
        txtarea.insert(END, dxf)
    if(val==7):
        txtarea.delete("1.0","end")
        txtarea.insert(END, vis)

    if(fName!=None ):  
        T.delete("1.0","end")
        T.insert(INSERT,str(fName))
        T.configure(fg="White",font=('Arial',13,"bold"))
        T.tag_configure("center", justify='center')
        T.tag_add("center", "1.0", "end")
    

# //file to create new window 
def openNewWindow():

    if fName==None or fName=="" :
            T.delete("1.0","end")
            T.insert(INSERT,"Please Select the File")
            T.configure(fg="black",font="13")
            T.tag_configure("center", justify='center')
            T.tag_add("center", "1.0", "end")
            return

    if(var.get()==0):
            T.delete("1.0","end")
            T.insert(INSERT,"Select any Mode")
            T.configure(fg="black",font="13")
            T.tag_configure("center", justify='center')
            T.tag_add("center", "1.0", "end") 
            return  
            

    else:
          
        val=var.get()
        fExt = os.path.splitext(fName)[1]

        if(val==1 or val==2 or val==3 or val==4):
             if(fExt=='.jpg' or fExt=='.png'):
                root.destroy() 
                CBG.openffg(fName,val)
             else:
                T.delete("1.0","end")
                T.insert(INSERT,"Choose Right Formate *.jpg or *.png")
                T.configure(fg="black",font="13")
                T.tag_configure("center", justify='center')
                T.tag_add("center", "1.0", "end")
                return 

        if(val==5):
            if(fExt=='.svg'):
                 root.destroy() 
                 svg2G.svg(fName)
            else:
                T.delete("1.0","end")
                T.insert(INSERT,"Choose Right Formate *.svg ")
                T.configure(fg="black",font="13")
                T.tag_configure("center", justify='center')
                T.tag_add("center", "1.0", "end")
                return 
            
        if(val==6):
            if(fExt=='.dxf'):
                 root.destroy() 
                 dxf2G.dxfcall(fName)
            else:
                T.delete("1.0","end")
                T.insert(INSERT,"Choose Right Formate *.dxf")
                T.configure(fg="black",font="13")
                T.tag_configure("center", justify='center')
                T.tag_add("center", "1.0", "end")
                return 
            
        if(val==7):
            if(fExt=='.gcode'):
                 root.destroy() 
                 ln=len(fName)
                 Edittor.fileReader(fName[0:ln-13])
            else:
                T.delete("1.0","end")
                T.insert(INSERT,"Choose Right Formate *.gcode")
                T.configure(fg="black",font="13")
                T.tag_configure("center", justify='center')
                T.tag_add("center", "1.0", "end")
                return 

              
            
fName=None
root = Tk()
root.title('Setup.ex')
root.resizable(False, False)

root['bg']='#4aa96c'
Label(root, text ="Gcode Generator",font=('Baskerville ',23,'bold'),foreground="white",background="#4aa96c").pack(padx=15)     
     
canvas = Canvas(root, width = 450, height = 100)      
canvas.pack(pady=25,expand=1,fill=BOTH)
img = PhotoImage(file="dir_in/logo.png")  
canvas.create_image(240,50, image=img)    

canvas2 = Canvas(root, width =200, height =-2) 
canvas2.pack(fill=BOTH,expand=1,pady=15)
# canvas2.create_line(15, 25, 200, 25)


tb=Label(root, text ="@ Naveed_Aamir (2020-2021)",font=('italic',12,'bold'),foreground="#fdfaf6",background="#4aa96c")
tb.pack(side=BOTTOM,anchor=CENTER)

canvas4 = Canvas(root, width =200, height =-2) 
canvas4.pack(fill=BOTH,expand=1,side=BOTTOM,anchor=CENTER,pady=5)

btn = Button(root, text ="Next",width=20, command = openNewWindow).pack(anchor=CENTER,side=BOTTOM,pady=25,expand=True) 
open_button = Button(root,text='Select File',width=36,command=select_file)
open_button.pack()

canvas3 = Canvas(root, width =200, height =-2) 
canvas3.pack(fill=BOTH,expand=1,pady=15)
T = Text(root, height = 1, width = 32,foreground='black',font=(10),relief="flat",background='#4aa96c')
T.pack(pady=25)


frame = Frame(root)
frame['borderwidth'] = 2
frame['relief'] = 'sunken'
frame.pack(padx=25,anchor=NE,side=RIGHT)

txtarea = Text(frame,width=20,  borderwidth=8,height=8,background="black",foreground="#39FF14",font=('Courier',10,'bold'))
txtarea.pack(ipadx=20)
txtarea.insert(END,"Please \nChoose\nAny OPTION !")



var = IntVar()
s = Style().configure('Wild.TRadiobutton',background="#4aa96c",font=('Arial',13), foreground='white') 
R1 = Radiobutton(root, text="Raster-Gcode",style='Wild.TRadiobutton',variable=var, value=1,command=sel)
R2 = Radiobutton(root, text="Matrix Function",style='Wild.TRadiobutton',variable=var, value=2,command=sel)
R3 = Radiobutton(root, text="Hash Printing",style='Wild.TRadiobutton',variable=var, value=3,command=sel)
R4 = Radiobutton(root, text="Dot Printing",style='Wild.TRadiobutton',variable=var, value=4,command=sel)
R5 = Radiobutton(root, text="SVG To Gcode",style='Wild.TRadiobutton',variable=var, value=5,command=sel)
R6 = Radiobutton(root, text="DXF To Gcode",style='Wild.TRadiobutton',variable=var, value=6,command=sel)
R7 = Radiobutton(root, text="G-code Sender",style='Wild.TRadiobutton',variable=var, value=7,command=sel)
R1.pack( padx=25,anchor=W)
R2.pack( padx=25,anchor=W)
R3.pack( padx=25,anchor=W)
R4.pack( padx=25,anchor=W)
R5.pack( padx=25,anchor=W)
R6.pack( padx=25,anchor=W)
R7.pack( padx=25,anchor=W)

  
root.mainloop()
