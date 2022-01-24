# from PIL import Image

# img = Image.open('test.jpg')
# imgGray = img.convert('L')
# imgGray.save('test_gray.jpg')
import cv2
import os
import RasterComp
import line2G
import Dot2G
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

fName=None
b=None
c=None
final=None
final2=None

def BrightnessContrast(brightness=0):
    
    global final,final2,c,b
    brightness = cv2.getTrackbarPos('Brightness','Press Q-Save&Quit and G-GrayScale')  
    contrast = cv2.getTrackbarPos('Contrast','Press Q-Save&Quit and G-GrayScale')
    effect = controller(final, brightness, contrast)
    final2=effect
    c=contrast
    b=brightness
    cv2.imshow('Press Q-Save&Quit and G-GrayScale', effect)

def controller(final, brightness=255,contrast=127):
    brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))
    contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))

    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            max = 255
        else:
            shadow = 0
            max = 255 + brightness
        al_pha = (max - shadow) / 255
        ga_mma = shadow
        cal = cv2.addWeighted(final, al_pha,final, 0, ga_mma)
    else:
        cal = final

    if contrast != 0:
        Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
        Gamma = 127 * (1 - Alpha)
        cal = cv2.addWeighted(cal, Alpha, cal, 0, Gamma)
    return cal  
# //file to create new window 
def openffg(fName,mode) :

 
    
    global final,final2
    img = cv2.imread(fName,cv2.IMREAD_UNCHANGED)
    final=img
    # //dimension of image adjust if large;
    ww=img.shape[0]
    hh=img.shape[1]
    print(hh,ww) 
    if(hh>=300 or ww>=600):

        diff=max(((hh-300)*100)/hh,((ww-600)*100)/ww)
        scale_percent =100- diff
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        
        dsize = (width, height)
        final = cv2.resize(img, dsize)

    
    cv2.namedWindow('Press Q-Save&Quit and G-GrayScale')   
    cv2.createTrackbar('Brightness','Press Q-Save&Quit and G-GrayScale', 255, 2 * 255,BrightnessContrast) 
    cv2.createTrackbar('Contrast', 'Press Q-Save&Quit and G-GrayScale',127, 2 * 127,BrightnessContrast)
    # cv2.createTrackbar('G-To convert into gray', 'Setup.ex',0, 0,BrightnessContrast)
    BrightnessContrast(0)

    
    key = cv2.waitKey(0) & 0xFF

    if key == ord('g') :

        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        final=cv2.cvtColor(final,cv2.COLOR_BGR2GRAY)
        cv2.imshow('Press Q-Save&Quit and G-GrayScale',final)
        key2 = cv2.waitKey(0) & 0xFF
  
        if key2 == ord('q'):
            cv2.imwrite('dir_in/resize.jpg',final2)
            effected = controller(img,b,c)
            cv2.imwrite('dir_in/savedImage1000x.jpg',effected)
            cv2.destroyAllWindows()

            # //////all mode 1-4 from here 
            if(mode==1):RasterComp.band(mode)
            if(mode==2):RasterComp.band(mode)
            if(mode==3):line2G.bandline()
            if(mode==4):Dot2G.bandline2()


    if key == ord('q'):

        cv2.imwrite('dir_in/resize.jpg',final2)
        effected = controller(img,b,c)
        cv2.imwrite('dir_in/savedImage1000x.jpg',effected)
        cv2.destroyAllWindows()

        # //////all mode 1-4 from here 
        if(mode==1):RasterComp.band(mode)
        if(mode==2):RasterComp.band(mode)
        if(mode==3):line2G.bandline()
        if(mode==4):Dot2G.bandline2()




# openffg("dir_in/ddd.jpg",1)    