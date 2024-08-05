from tkinter import *
import os

class GUI:
    def __init__(self):
        self.__form__ = Tk()
        self.__form__.geometry('800x550')
        self.__form__.title('StandArt')
        self.__form__.resizable(0, 0) # user couldn't change size of window

        if os.name != 'posix':
        	self.__form__.iconbitmap('icon.ico')

        self.set_menu()
        self.set_ui()

    
    def set_menu(self):
        self.__main_menu__ = Menu(self.__form__)
        self.__form__.configure(menu = self.__main_menu__)

        self.__options_item__ = Menu(self.__main_menu__)
        self.__main_menu__.add_cascade(label = 'File', menu = self.__options_item__)

    
    def set_ui(self):
        self.canvas = Canvas(self.__form__, bg = 'white', width = self.__form__.winfo_width () - 50, height = self.__form__.winfo_height () - 120)
        self.canvas.grid(row = 1, column = 0, columnspan = 10, padx = 5, pady = 5, sticky = E+W+S+N)

        self.brush_size = Scale(self.__form__, from_ = 0, to = 100, orient = HORIZONTAL)
        self.brush_size.grid(row = 0, column = 8)
        
        self.clear_button = Button(self.__form__, text = 'Clear', width = 10, bg = 'white')
        self.clear_button.grid(row = 2, column = 8)
 
        self.erase_button = Button(self.__form__, text = 'Erase', width = 10, bd = 1, bg = 'white')
        self.erase_button.grid (row = 2, column = 9)


    def set_colors(self, colors, set_color_func):
        self.__colors__ = []
        for color in colors:
            self.__colors__.append(Button(self.__form__, bg = color, bd = 1, width = 5, height = 3, command = lambda color=color: set_color_func(color)))
            self.__colors__[-1].grid(row = 0, column = colors.index(color))


    def add_option(self, name, command):
        self.__options_item__.add_command(label = name, command = command)


    def keyboard(self, main_key, keys, command):
        for key in keys:
            self.__form__.bind(f'<{main_key}-{key}>', command)
    

    def mouse_motion(self, command):
        self.canvas.bind ('<B1-Motion>', command)
        self.canvas.bind ('<Button-1>', command)
    

    def clear(self, command):
        self.clear_button.config(command = command)


    def erase(self, command):
        self.erase_button.config(command = command)


    def on_closing(self, command):
        self.__form__.protocol('WM_DELETE_WINDOW', command)


    def update(self):
        self.__form__.update()
        self.__form__.update_idletasks()


    def destroy(self):
        self.__form__.destroy()
    

    def form_scale(self):
        return (self.__form__.winfo_rootx(), self.__form__.winfo_rooty())
    

    def canvas_scale(self):
        return (self.canvas.winfo_x(), self.canvas.winfo_y())
    

    def canvas_width(self):
        return self.canvas.winfo_width()
    

    def canvas_height(self):
        return self.canvas.winfo_height()