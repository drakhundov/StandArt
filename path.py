from tkinter import filedialog
import os, sys


class File:
    def __init__ (self):
        self.__filetypes = FileTypes([('StandArt Files', '*.art'), ('PNG Files', '*.png')])
        self.__saved = True
        self.__path = ''


    def select_path(self, mode, new_place = False):
        if self.__path == '' or new_place:
            if mode == 'save': path = filedialog.asksaveasfilename(initialdir = '/', title = 'Save Your Art', filetypes = self.__filetypes.get('all'))
            elif mode == 'open': path = filedialog.askopenfilename(initialdir = '/', title = 'Open Art File', filetypes = self.__filetypes.get('art'))
            
            if path != '':
                return path
            
            else:
                return None
    

    def get_path(self):
        if self.__path != '':
            return self.__path
        
        else:
            return None


    def set_path(self, path):
        if path is not None:
            self.__path = path


    def set_saved(self, saved):
        self.__saved = saved


    def is_saved(self):
        return self.__saved



class FileTypes:
    def __init__(self, filetypes):
        self.__filetypes = filetypes
    

    def get(self, filetype):
        if filetype == 'all': return self.__filetypes

        for ft in self.__filetypes:
            if ft[1] == f'*.{filetype}':
                return [ft]