# Made By Abdul Akhundzada
# Copyright 2020
# Baku, AZ

from tkinter import *
from tkinter import messagebox
import sys
from typing import Optional, List

from gui import GUIConstructor
from filemng import OSFileManager
from brush import Brush
from picture import Picture


class Main:
    def __init__(self):
        self.gui_constructor = GUIConstructor()
        self.file_mng = OSFileManager()
        self.brush = Brush()
        self.pic = Picture()

        self.gui_constructor.set_callback(
            "keyboard_conf",
            self.keyboard_callback,
            main_key="Command" if sys.platform == "darwin" else "Control",
            keys=("s", "o", "z"),
        )
        self.gui_constructor.set_callback("on_closing", self.on_closing)
        self.gui_constructor.set_callback("mouse_motion", self.mouse_motion_callback)
        self.gui_constructor.set_callback("clear", self.clear_btn_callback)
        self.gui_constructor.set_callback("erase", self.erase_btn_callback)
        self.gui_constructor.set_callback("save_file", self.save)
        self.gui_constructor.set_callback("save_as", lambda: self.save(new_file=True))
        self.gui_constructor.set_callback("open_file", self.open)

        self.gui_constructor.set_color_buttons(
            self.brush.get_colors(), self.brush.set_color
        )
        self.gui_constructor.brush_size_scale.config(command=self.brush.set_size)

    def save(self, new_file: bool = False):
        success = self.file_mng.save(pic_obj=self.pic, is_new_path=new_file)
        if not success:
            messagebox.showwarning("Save Cancelled", "File save was cancelled.")

    def open(self, path: Optional[str] = None):
        if not self.file_mng.is_saved() and messagebox.askyesno(
            "Save Current Picture?"
        ):
            self.save()

        pic = self.file_mng.open(path)

        # User cancelled the file dialog.
        if pic is None:
            return

        self.pic.clear()
        self.gui_constructor.canvas.delete("all")
        for element in pic.get():
            coords = element[:4]
            color = self.brush.get_colors()[element[-1]]
            self.draw(coords, color)

    def draw(
        self,
        coords: List[int],
        color: str,
        canvas: bool = True,
        pic: bool = True,
        file_changed: bool = False,
    ):
        if canvas:
            self.gui_constructor.canvas.create_oval(
                coords[0], coords[1], coords[2], coords[3], fill=color, outline=color
            )
        if pic:
            self.pic.add(coords, self.brush.get_colors().index(color))
        if file_changed:
            self.file_mng.set_saved(False)

    def erase(self, coords):
        ovals = self.gui_constructor.canvas.find_overlapping(
            coords[0], coords[1], coords[2], coords[3]
        )

        if len(ovals) > 0:
            self.gui_constructor.canvas.delete(ovals[0])
            self.pic.delete(coords)
            self.file_mng.set_saved(False)

    def last(self):
        if len(self.pic.get()) >= 1:
            elements = self.gui_constructor.canvas.find_overlapping(
                self.pic.get()[-1][-5],
                self.pic.get()[-1][-4],
                self.pic.get()[-1][-3],
                self.pic.get()[-1][-2],
            )

            self.pic.delete(self.gui_constructor.canvas.coords(elements[-1]))
            self.gui_constructor.canvas.delete(elements[-1])
            self.file_mng.set_saved(False)

    def update(self):
        self.gui_constructor.update()

    def clear_btn_callback(self):
        self.pic.clear()
        self.gui_constructor.canvas.delete("all")
        self.file_mng.set_saved(False)

    def erase_btn_callback(self):
        if (
            self.gui_constructor.erase_button.cget("bg") == "white"
            and self.gui_constructor.erase_button.cget("bd") == 1
        ):
            self.gui_constructor.erase_button.config(bg="blue", bd=3)
            self.brush.set_mode("erase")
        elif (
            self.gui_constructor.erase_button.cget("bg") == "blue"
            and self.gui_constructor.erase_button.cget("bd") == 3
        ):
            self.gui_constructor.erase_button.config(bg="white", bd=1)
            self.brush.set_mode("draw")

    def on_closing(self):
        if not self.file_mng.is_saved() and messagebox.askyesno("Save changes?"):
            self.save()
        self.gui_constructor.destroy()

    def keyboard_callback(self, event):
        if event.keysym == "s":
            self.save()

        elif event.keysym == "o":
            self.open()

        elif event.keysym == "z":
            self.last()

    def mouse_motion_callback(self, event):
        coords = [
            event.x - self.brush.get_size(),
            event.y - self.brush.get_size(),
            event.x + self.brush.get_size(),
            event.y + self.brush.get_size(),
        ]
        draw_mode = self.brush.get_mode()
        if draw_mode == "draw":
            self.draw(coords, self.brush.get_color())
        elif draw_mode == "erase":
            self.erase(coords)
        self.file_mng.set_saved(False)


program = Main()

# if '*.art' file in OS is opened
if len(sys.argv) > 1:
    program.open(sys.argv[1])


while True:
    try:
        program.update()
    except:
        break
