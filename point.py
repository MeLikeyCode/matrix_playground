from mathobject import MathObject
import config
from config import LABEL_FONT
from vector import Vector

class Point(MathObject):
    """A 2d point."""
    def __init__(self, x, y, label=None):
        super().__init__()
        self._point = (x, y)
        self._label = label

    def copy(self):
        return Point(self._point[0], self._point[1])

    def draw(self):
        transformed = config.command_interpretter.initial_transform * Vector(self._point[0], self._point[1])
        o = self._canvas.create_oval(
            transformed[0] - 3,
            transformed[1] - 3,
            transformed[0] + 3,
            transformed[1] + 3,
            fill=self._color,
            outline=self._color,
        )
        self._canvas_items.append(o)

        if self._label is not None:
            t = self._canvas.create_text(
                transformed[0] + 10,
                transformed[1] + 10,
                text=self._label,
                font=LABEL_FONT,
                fill=self._color
            )
            self._canvas_items.append(t)

    def __add__(self, other):
        if isinstance(other, Vector):
            return Point(
                self._point[0] + other._vector[0], self._point[1] + other._vector[1]
            )

        return NotImplemented

    @property
    def x(self):
        return self._point[0]

    @property
    def y(self):
        return self._point[1]

    def __getitem__(self, key):
        return self._point[key]
