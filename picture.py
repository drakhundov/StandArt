from typing import List, Optional


class Picture:
    """
    The picture is represented by an array of integer arays.
    Every integer array represents a point in the picture that was drawn:
        first 4 elements => "coords"
        last element     => "colorID
    """
    def __init__(self, image_array: Optional[List] = None):
        if image_array is not None:
            for pnt in image_array:
                if len(pnt) != 5:
                    raise ValueError(
                        "[Picture::__init__]: invalid array of elements: ", image_array
                    )
        self.img_arr = image_array or []

    def get(self):
        return self.img_arr

    def add(self, coords, colorID):
        self.img_arr.append(coords + [colorID])

    def delete(self, coords):
        for element in self.img_arr:
            if element[:4] == coords:
                self.img_arr.remove(element)

    def clear(self):
        self.img_arr.clear()
