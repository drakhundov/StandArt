import os
import pickle
from typing import Literal, Optional

from tkinter import filedialog

from picture import Picture


class OSFileManager:
    def __init__(self):
        self.FILETYPES = tuple(
            ("StandArt Files", "*.art"),
        )
        self.file_saved: bool = True
        self.path: str

    def select_path(
        self, mode: Literal["save", "open"], is_new_path: bool = False
    ) -> Optional[str]:
        if self.path == "" or is_new_path:
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
            print("File path has already been established.")
            return None

    def save(self, pic_obj: Picture, is_new_path: bool):
        path: str
        is_valid_path: bool
        if (self.get_path() is None or is_new_path) and (
            (path := self.select_path("save")) is not None and
            (is_valid_path := os.path.exists(path))
        ):
            self.set_path(path)
        elif not is_valid_path:
            raise OSError("[OSFileManager:save] Invalid path: ", path)
        else:
            return

        extension = os.path.splitext(path)[1]
        if extension == ".art":
            with open(path, "wb") as f:
                pickle.dump(pic_obj.get(), f)

        self.set_saved(True)

        # elif extension == ".png":
        #     form_scale = self.ui.form_scale()
        #     canvas_scale = self.ui.canvas_scale()

        #     x1 = form_scale[0] + canvas_scale[0]
        #     y1 = form_scale[1] + canvas_scale[1]
        #     x2 = x1 + self.ui.canvas_width()
        #     y2 = y1 + self.ui.canvas_height()

        #     ImageGrab.grab().crop((x1, y1, x2, y2)).save(self.file.get_path())

    def get_path(self) -> Optional[str]:
        if self.path != "":
            return self.path
        else:
            return None

    def set_path(self, path: str):
        if path is not None:
            self.path = path

    def set_saved(self, saved: bool):
        self.file_saved = saved

    def is_saved(self) -> bool:
        return self.file_saved
