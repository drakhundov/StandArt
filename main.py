# Made By Abdul Akhundzade
# Copyright 2020
# Baku, AZ

from tkinter import *
from tkinter import messagebox
import os, sys
import pickle

from gui import GUI
from path import File
from draw import Brush
from image import Image

try:
	from PIL import ImageGrab
except:
	pass


# if file is launched by user, change dir to script directory
if sys.argv[0] != __file__: os.chdir(os.path.dirname(sys.argv[0])) 


class StandArt:
    def __init__(self):
        self.ui = GUI()
        self.file = File()
        self.brush = Brush()
        self.image = Image()

        self.ui.keyboard('Control', ('s', 'o', 'z'), self.__keyboard__)
        self.ui.mouse_motion(self.__mouse_motion__)
        self.ui.on_closing(self.__on_closing__)
        self.ui.clear(self.__clear_button__)
        self.ui.erase(self.__erase_button__)

        self.ui.add_option('Save', self.save)
        self.ui.add_option('Save As', lambda: self.save(new_file = True))
        self.ui.add_option('Open', self.open)

        self.ui.set_colors(self.brush.get_colors(), self.brush.set_color)
        self.ui.brush_size.config(command = self.brush.set_size)


    def save(self, new_file = False):
        if (self.file.get_path() is None or new_file) and ((path := self.file.select_path('save')) is not None):
            self.file.set_path(path)

        else: 
            return
        
        path = self.file.get_path()
        extension = os.path.splitext(path)[1]

        if extension == '.art':
            with open(self.file.get_path(), 'wb') as art_file:
                pickle.dump(self.image.get(), art_file)

        elif extension == '.png':
            form_scale = self.ui.form_scale()
            canvas_scale = self.ui.canvas_scale()

            x1 = form_scale[0] + canvas_scale[0]
            y1 = form_scale[1] + canvas_scale[1]
            x2 = x1 + self.ui.canvas_width()
            y2 = y1 + self.ui.canvas_height()

            ImageGrab.grab ().crop((x1, y1, x2, y2)).save (self.file.get_path())
        
        self.file.set_saved(True)

    
    def open(self, path = ''):
        if not self.file.is_saved() and messagebox.askyesno('Save Current Picture?'): self.save()

        if path == '':
            path = self.file.select_path('open')

        self.file.set_path(path)

        extension = os.path.splitext(path)[1]

        if extension == '.art':
            with open(self.file.get_path(), 'rb') as art_file:
                image = Image(pickle.load(art_file))

                self.image.clear()
                self.ui.canvas.delete('all')

                for element in image.get():
                    coords = element[:4]
                    color = self.brush.get_colors()[element[-1]]
                    self.draw(coords, color)
            
            self.file.set_saved(True)


    def draw(self, coords, color):
        self.ui.canvas.create_oval (coords[0], coords[1],
                                    coords[2], coords[3],
                                    fill = color, outline = color)

        self.image.add(coords, self.brush.get_colors().index(color))

        self.file.set_saved(False)


    def erase(self, coords):
        ovals = self.ui.canvas.find_overlapping (coords[0], coords[1],
                                                 coords[2], coords[3])

        if len (ovals) > 0: 
            self.ui.canvas.delete(ovals[0])
            self.image.delete(coords)

            self.file.set_saved(False)
    

    def last(self):
        if len (self.image.get()) >= 1:
            elements = self.ui.canvas.find_overlapping (self.image.get()[-1][-5], self.image.get()[-1][-4],
                                                        self.image.get()[-1][-3], self.image.get()[-1][-2])
            
            self.image.delete(self.ui.canvas.coords(elements[-1]))
            self.ui.canvas.delete(elements[-1])

            self.file.set_saved(False)
    

    def __clear_button__(self):
        self.image.clear()
        self.ui.canvas.delete('all')
        self.file.set_saved(True)


    def __erase_button__(self):
        if self.ui.erase_button.cget('bg') == 'white' and self.ui.erase_button.cget('bd') == 1:
            self.ui.erase_button.config(bg = 'blue', bd = 3)
            self.brush.set_mode('erase')

        elif self.ui.erase_button.cget('bg') == 'blue' and self.ui.erase_button.cget('bd') == 3:
            self.ui.erase_button.config(bg = 'white', bd = 1)
            self.brush.set_mode('draw')


    def update(self):
        self.ui.update()


    def __on_closing__(self):
        if not self.file.is_saved() and messagebox.askyesno('Save changes?'): self.save()
    
        self.ui.destroy()


    def __keyboard__(self, event):
        if event.keysym == 's': self.save()
        
        elif event.keysym == 'o': self.open()
        
        elif event.keysym == 'z': self.last()


    def __mouse_motion__(self, event):
        coords = [event.x - self.brush.get_size(), event.y - self.brush.get_size(),
                  event.x + self.brush.get_size(), event.y + self.brush.get_size()]

        draw_mode = self.brush.get_mode()
        if draw_mode == 'draw': self.draw(coords, self.brush.get_color())
        elif draw_mode == 'erase': self.erase(coords)

        self.file.set_saved(False)



program = StandArt()

# if '*.art' file in OS is opened
if len(sys.argv) > 1: program.open(sys.argv[1])


while True: 
    try: program.update()
    except: break