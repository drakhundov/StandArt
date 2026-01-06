from typing import Literal, Optional

from tkinter import filedialog


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
