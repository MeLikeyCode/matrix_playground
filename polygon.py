from mathobject import MathObject
import config
from config import LABEL_FONT
from vector import Vector

class Polygon(MathObject):
    """A polygon."""

    @staticmethod
    def rectangle(x,y,w,h):
        return Polygon([(x,y), (x+w,y), (x+w,y+h), (x,y+h)])

    @staticmethod
    def square(x,y,s):
        return Polygon.rectangle(x,y,s,s)

    @staticmethod
    def triangle(x,y,w,h):
        return Polygon([(x,y), (x+w,y), (x+w/2,y+h)])

    def __init__(self, points, label=None):
        super().__init__()
        self._points = points
        self._label = label
        self._points_transformed = [config.command_interpretter.initial_transform * Vector(p[0], p[1]) for p in points]

    def copy(self):
        return Polygon(self._points)

    def draw(self):
        xys = [p for pt in self._points_transformed for p in pt]
        p = self._canvas.create_polygon(
            *xys,
            fill=self._color
        )
        self._canvas_items.append(p)

        if self._label is not None:
            text_x = sum([p[0] for p in self._points]) / len(self._points)
            text_y = sum([p[1] for p in self._points]) / len(self._points)
            pt_transformed = config.command_interpretter.initial_transform * Vector(text_x, text_y)
            t = self._canvas.create_text(
                pt_transformed[0],
                pt_transformed[1],
                text=self._label,
                font=LABEL_FONT,
                fill='#fff', # label and polygon have to be different colors
            )
            self._canvas_items.append(t)