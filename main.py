from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import cv2
import numpy as np
import matplotlib.pyplot as plt

main = tkinter.Tk()
main.title("Recovery Of Image Using One dimensional Signal")
main.geometry("1000x700")#width*height

global damage, mask
global one_dim_psnr, two_dim_psnr


def uploadDamage():
    global damage
    damage = filedialog.askopenfilename(initialdir="images")
    pathlabel.config(text=damage)
    text.delete('1.0', END)
    text.insert(END,damage+" loaded\n");
   

def uploadMask():
    global mask
    mask = filedialog.askopenfilename(initialdir="images")
    pathlabel.config(text=mask)
    text.insert(END,mask+" loaded\n\n");
   
def twoDimensionRestoration():
    global two_dim_psnr, damage, mask
    img = cv2.imread(damage)
    mask_img = cv2.imread(mask,0)
    img = cv2.resize(img, (400,400))
    mask_img = cv2.resize(mask_img, (400,400))
    restore = cv2.inpaint(img,mask_img,3,cv2.INPAINT_NS)
    two_dim_psnr = cv2.PSNR(img, restore, 255)
    text.insert(END,"Two dimensional image restoration PSNR : "+str(two_dim_psnr)+"\n\n")
    
    cv2.imshow("original image", img)
    cv2.imshow("mask",mask_img)
    cv2.imshow("Restoration Image",restore)
    cv2.waitKey(0)

def oneDimensionRestoration():
    global one_dim_psnr, damage, mask
    img = cv2.imread(damage)
    mask_img = cv2.imread(mask,0)
    img = cv2.resize(img, (400,400))
    mask_img = cv2.resize(mask_img, (400,400))
    restore =  cv2.inpaint(img,mask_img,3,cv2.INPAINT_TELEA)
    one_dim_psnr = cv2.PSNR(img, restore, 255)
    text.insert(END,"One dimensional image restoration PSNR : "+str(one_dim_psnr)+"\n\n")
    
    cv2.imshow("original image", img)
    cv2.imshow("mask",mask_img)
    cv2.imshow("Restoration Image",restore)
    cv2.waitKey(0)
    
def graph():
    global one_dim_psnr, two_dim_psnr
    height = [one_dim_psnr, two_dim_psnr]
    bars = ('One Dimension PSNR','Two Dimension PSNR')
    y_pos = np.arange(len(bars))
    plt.bar(y_pos, height)
    plt.xticks(y_pos, bars)
    plt.title("One & Two Dimension Image Restoration PSNR Comparison Graph")
    plt.show()
    
font = ('times', 16, 'bold')
title = Label(main, text='Recovery Of Image Using One Dimensional Signal')
title.config(bg='light cyan', fg='pale violet red')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 14, 'bold')
damageButton = Button(main, text="Upload Damaged Image", command=uploadDamage)
damageButton.place(x=50,y=100)
damageButton.config(font=font1)  

pathlabel = Label(main)
pathlabel.config(bg='light cyan', fg='pale violet red')  
pathlabel.config(font=font1)           
pathlabel.place(x=460,y=100)

maskButton = Button(main, text="Upload Mask Image", command=uploadMask)
maskButton.place(x=50,y=150)
maskButton.config(font=font1) 

twoButton = Button(main, text="Two Dimensional Restoration", command=twoDimensionRestoration)
twoButton.place(x=330,y=150)
twoButton.config(font=font1)

oneButton = Button(main, text="One Dimensional Restoration", command=oneDimensionRestoration)
oneButton.place(x=50,y=200)
oneButton.config(font=font1)

graphButton = Button(main, text="PSNR Graph", command=graph)
graphButton.place(x=330,y=200)
graphButton.config(font=font1)



font1 = ('times', 12, 'bold')
text=Text(main,height=20,width=150)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=10,y=250)
text.config(font=font1)


main.config(bg='snow3')
main.mainloop()