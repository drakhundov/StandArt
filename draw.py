class Brush:
    def __init__(self):
        self.__colors = ['red', 'blue', 'green', 'black', 'yellow', 'orange']
        self.__color = 'black'

        self.__minSize = 0
        self.__maxSize = 100
        self.__size = 0

        self.__mode = DrawMode()


    def get_color(self):
        return self.__color


    def set_color(self, color):
        if color in self.__colors:
            self.__color = color
    

    def get_size(self):
        return self.__size


    def set_size(self, size):
        if self.__minSize <= int(size) <= self.__maxSize:
            self.__size = int(size)
    

    def get_mode(self):
        return self.__mode.get()


    def set_mode(self, mode):
        self.__mode.changeTo(mode)


    def get_colors(self):
        return self.__colors



class DrawMode:
    def __init__ (self):
        self.__modes = ['draw', 'erase']
        self.__mode = 'draw'


    def get (self): return self.__mode
    
    def changeTo (self, mode): 
        if mode in self.__modes: self.__mode = mode