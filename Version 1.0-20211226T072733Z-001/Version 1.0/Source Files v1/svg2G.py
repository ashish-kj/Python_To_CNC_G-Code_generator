from tkinter import *
from tkinter import ttk
import time
from tkinter.ttk import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import Edittor
from tkinter import filedialog as fd
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces

fName=None

def svg2G(filename,fileO):

     gcode_compiler = Compiler(interfaces.Gcode, movement_speed=1000, cutting_speed=300, pass_depth=5)
     curves = parse_file(filename) # Parse an svg file into geometric curves
     gcode_compiler.append_curves(curves) 
     gcode_compiler.compile_to_file(fileO+"/output.gcode", passes=2)

def select_file():

    global fName  
    fName=fd.askdirectory()
    label.config(text = str(fName)) 


def convertFinal():

     if(fName=="" or fName==None):
        label.config(text = "Choose output Folder !")
        return   
     
     count=1 
     count2=1

     while(True):
          progress['value'] =count
          root.update_idletasks()
          time.sleep(.01)
          count=count+1
          count2=count2+1
          if(count==99):
               count=0
          if (count2>=50):
               break     
     
     svg2G(filename2,fName)
     
     while(True):
          progress['value'] =count
          root.update_idletasks()
          time.sleep(.05)
          count=count+1
          if(count==101):
               break
     
     root.destroy()
     Edittor.fileReader(fName)


def svg(filename):
     
     global root,progress,var,label,filename2
     filename2=filename

     root = Tk()
     root.title('Setup.ex') 
     root['bg']='#4aa96c'
     root.resizable(False, False)
 
     Label(root, text ="SVG Compilation", font=('Arial',20,'bold'),foreground="White",background="#4aa96c").pack()
     canvas2 = Canvas(root, width =200, height =0) 
     canvas2.pack(fill=BOTH,expand=1,pady=5)
    
     open_btn = Button(root,text='Output Location',width=16,command=select_file)
     open_btn.pack( anchor = CENTER,pady=10)

     label =Label(root,text="")
     label.pack(anchor =CENTER,padx=10,pady=5 )
     label.config(background="#4aa96c",justify='center',font=('Arial',13),foreground='white')


     canvas2 = Canvas(root, width =200, height =-4) 
     canvas2.pack(fill=BOTH,expand=1)
     progress = Progressbar(root, orient = HORIZONTAL,length =500, mode = 'determinate')
     progress.pack(pady =3)
     canvas2 = Canvas(root, width =200, height =-4) 
     canvas2.pack(fill=BOTH,expand=1)

     open_button =Button(root,text='Proceed',width=20,command=convertFinal)
     open_button.pack(pady=10,anchor=CENTER,padx=10)

     root.wm_protocol("WM_DELETE_WINDOW", root.destroy)
     root.mainloop()
    

# svg("sdfsdf")

