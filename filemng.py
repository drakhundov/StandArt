import os
import pickle
from typing import Literal, Optional

from tkinter import filedialog

from picture import Picture


class OSFileManager:
    def __init__(self):
        self.FILETYPES = (("StandArt Files", "*.art"),)
        self.file_saved: bool = True
        self.path: Optional[str] = None

    def select_path(
        self, mode: Literal["save", "open"], is_new_path: bool = False
    ) -> Optional[str]:
        if self.path is None or is_new_path:
            if mode == "save":
                path = filedialog.asksaveasfilename(
                    initialdir="/",
                    title="Save File",
                    filetypes=self.FILETYPES,
                )
            elif mode == "open":
                path = filedialog.askopenfilename(
                    initialdir="/",
                    title="Open File",
                    filetypes=self.FILETYPES,
                )
            if path != "":
                return path
            else:
                return None
        else:
            print("[OSFileManager.select_path] File path has already been established.")
            return None

    def save(self, pic_obj: Picture, is_new_path: bool = False) -> bool:
        """
        Save given Picture object.
        Returns True if saved successfully, False if cancelled or failed.
        """
        path: str
        if self.get_path() is None or is_new_path:
            path = self.select_path(mode="save", is_new_path=is_new_path)
            # User cancelled the dialog.
            if path is None:
                return False
            if not os.path.exists(os.path.dirname(path)):
                raise OSError("[OSFileManager.save] Invalid path: ", path)
            self.set_path(path)
        
        extension = os.path.splitext(self.path)[1]
        if extension == ".art":
            with open(self.path, "wb") as f:
                pickle.dump(pic_obj.get(), f)

        self.set_saved(True)
        return True
        # elif extension == ".png":
        #     form_scale = self.ui.form_scale()
        #     canvas_scale = self.ui.canvas_scale()

        #     x1 = form_scale[0] + canvas_scale[0]
        #     y1 = form_scale[1] + canvas_scale[1]
        #     x2 = x1 + self.ui.canvas_width()
        #     y2 = y1 + self.ui.canvas_height()

        #     ImageGrab.grab().crop((x1, y1, x2, y2)).save(self.file.get_path())

    def open(self, path: Optional[str] = None) -> Optional[Picture]:
        if path is None:
            path = self.select_path(mode="open", is_new_path=True)
        
        # User cancelled the dialog.
        if path is None:
            return None
            
        self.set_path(path)

        extension = os.path.splitext(path)[1]
        if extension == ".art":
            with open(self.get_path(), "rb") as f:
                pic = Picture(pickle.load(f))
            self.set_saved(True)
            return pic
        return None

    def get_path(self) -> Optional[str]:
        return self.path

    def set_path(self, path: str):
        if path is not None:
            self.path = path

    def set_saved(self, saved: bool):
        self.file_saved = saved

    def is_saved(self) -> bool:
        return self.file_saved
