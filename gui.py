from tkinter import *
import os
from typing import Literal, Callable, List


class GUIConstructor:
    def __init__(self):
        self.tk = Tk(useTk=True)
        # self.tk.geometry("1000x550")
        self.tk.title("StandArt")
        # self.__form__.resizable(0, 0)  # user couldn't change size of window

        if os.name != "posix":
            self.tk.iconbitmap("icon.ico")

        self.set_menu()
        self.set_ui()

    def set_menu(self):
        self.main_menu = Menu(self.tk)
        self.tk.configure(menu=self.main_menu)

        self.file_opts_submenu = Menu(self.main_menu)
        self.main_menu.add_cascade(label="File", menu=self.file_opts_submenu)

    def set_ui(self):
        self.canvas = Canvas(
            self.tk,
            bg="white",
            width=self.tk.winfo_screenwidth() * 0.5,
            height=self.tk.winfo_screenheight() * 0.5,
        )
        self.canvas.grid(
            row=1, column=0, columnspan=10, padx=5, pady=5, sticky=E + W + S + N
        )

        self.brush_size_scale = Scale(self.tk, from_=0, to=100, orient=HORIZONTAL)
        self.brush_size_scale.grid(row=0, column=8)

        self.clear_button = Button(self.tk, text="Clear", width=10, bg="white")
        self.clear_button.grid(row=2, column=8)

        self.erase_button = Button(self.tk, text="Erase", width=10, bd=1, bg="white")
        self.erase_button.grid(row=2, column=9)

    def set_color_buttons(self, colors: List[str], set_color_func: Callable):
        self.color_select_btn_lst = []
        for color in colors:
            # Use labels instead of buttons since MacOS
            # controls button style for consistency.
            new_lbl = Label(
                self.tk,
                bg=color,
                highlightthickness=0,
                bd=1,
                width=5,
                height=3,
                # command=lambda color=color: set_color_func(color),
            )
            self.color_select_btn_lst.append(new_lbl)
            new_lbl.bind("<Button-1>", lambda e, c=color: set_color_func(c))
            new_lbl.grid(row=0, column=colors.index(color))

    def set_callback(
        self,
        command: Literal[
            "erase",
            "clear",
            "mouse_motion",
            "on_closing",
            "keyboard_conf",
            "save_file",
            "open_file",
            "save_as",
        ],
        callback: Callable,
        *args,
        **kwargs,
    ):
        match command:
            case "erase":
                self.erase_button.config(command=callback)
            case "clear":
                self.clear_button.config(command=callback)
            case "mouse_motion":
                self.canvas.bind("<B1-Motion>", callback)
                self.canvas.bind("<Button-1>", callback)
            case "on_closing":
                self.tk.protocol("WM_DELETE_WINDOW", callback)
            case "keyboard_conf":
                keys = kwargs["keys"]
                main_key = kwargs["main_key"]
                for key in keys:
                    self.tk.bind(f"<{main_key}-{key}>", callback)
            case "save_file":
                self.file_opts_submenu.add_command(label="Save", command=callback)
            case "open_file":
                self.file_opts_submenu.add_command(label="Open", command=callback)
            case "save_as":
                self.file_opts_submenu.add_command(label="Save As", command=callback)

    def update(self):
        self.tk.update()
        self.tk.update_idletasks()

    def destroy(self):
        self.tk.destroy()

    def root_position(self):
        return (self.tk.winfo_rootx(), self.tk.winfo_rooty())

    def root_position(self):
        return (self.canvas.winfo_x(), self.canvas.winfo_y())

    def canvas_width(self):
        return self.canvas.winfo_width()

    def canvas_height(self):
        return self.canvas.winfo_height()
