#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
import tkinter as tk
import os
import pyscreenshot as ImageGrab
from PIL import Image, ImageTk, ImageEnhance
import random
import tempfile
import string
tempdir = tempfile.mkdtemp(prefix="clipit-")
root = tk.Tk()
root.resizable(0, 0)
root.title("Clip It")
def area_sel():
    x1 = y1 = x2 = y2 = 0
    roi_image = None
    def on_mouse_down(event):
        nonlocal x1, y1
        x1, y1 = event.x, event.y
        canvas.create_rectangle(x1, y1, x1, y1, outline='red', tag='roi')
    def on_mouse_move(event):
        nonlocal roi_image, x2, y2
        x2, y2 = event.x, event.y
        canvas.delete('roi-image')
        roi_image = image.crop((x1, y1, x2, y2)) 
        canvas.image = ImageTk.PhotoImage(roi_image)
        canvas.create_image(x1, y1, image=canvas.image, tag=('roi-image'), anchor='nw')
        canvas.coords('roi', x1, y1, x2, y2)
        canvas.lift('roi') 
    root.withdraw() 
    image = ImageGrab.grab()  
    bgimage = ImageEnhance.Brightness(image).enhance(0.3)  
    win = tk.Toplevel()
    win.attributes('-fullscreen', 1)
    win.attributes('-topmost', 1)
    canvas = tk.Canvas(win, highlightthickness=0)
    canvas.pack(fill='both', expand=1)
    tkimage = ImageTk.PhotoImage(bgimage)
    canvas.create_image(0, 0, image=tkimage, anchor='nw', tag='images')
    win.bind('<ButtonPress-1>', on_mouse_down)
    win.bind('<B1-Motion>', on_mouse_move)
    win.bind('<ButtonRelease-1>', lambda e: win.destroy())
    win.bind('<Escape>', lambda e: win.destroy())
    win.focus_force()
    win.grab_set()
    win.wait_window(win)
    root.deiconify() 
    if roi_image:
        letters = string.ascii_lowercase
        raw_image = ( ''.join(random.choice(letters) for i in range(10)) )
        roi_image.save(tempdir+'/'+raw_image + '.png')
        os.system('xclip -selection clipboard -t image/png -i '+ tempdir + '/' + raw_image + '.png &')
        exit()
tk.Button(root, text='Select', width=15, command=area_sel).pack()
root.mainloop()
