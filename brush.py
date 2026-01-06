from typing import Literal, get_args

# Define the accepted brush colors at the type level.
# Note: Literal values must be enumerated explicitly for static type checkers.
BrushColor = Literal["red", "blue", "green", "black", "yellow", "orange"]


class Brush:
    COLORS: tuple[BrushColor, ...] = get_args(BrushColor)

    def __init__(self):
        self.cur_color = "black"

        self.MINSIZE = 0
        self.MAXSIZE = 100
        self.size = 0

        self.mode = BrushMode()

    def get_color(self) -> BrushColor:
        return self.cur_color

    def set_color(self, color: BrushColor):
        if color in self.COLORS:
            self.cur_color = color

    def get_size(self) -> int:
        return self.size

    def set_size(self, size: int):
        if self.MINSIZE <= int(size) <= self.MAXSIZE:
            self.size = int(size)

    def get_mode(self) -> BrushMode:
        return self.mode.get()

    def set_mode(self, mode: BrushMode):
        self.mode.changeTo(mode)

    def get_colors(self):
        return self.COLORS


class BrushMode:
    def __init__(self):
        self.__modes = ["draw", "erase"]
        self.__mode = "draw"

    def get(self):
        return self.__mode

    def changeTo(self, mode):
        if mode in self.__modes:
            self.__mode = mode
