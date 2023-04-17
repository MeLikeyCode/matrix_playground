from mathobject import MathObject
import config
from config import LABEL_FONT
import numpy as np
from vector import Vector
from point import Point
import tkinter as tk
from polyline import Polyline
from polygon import Polygon

class LinearT(MathObject):
    @staticmethod
    def identity():
        return LinearT([[1, 0], [0, 1]])
    
    @staticmethod
    def rotation(angle):
        angle = np.radians(angle)
        return LinearT([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])

    @staticmethod
    def scaling(sx, sy):
        return LinearT([[sx, 0], [0, sy]])

    def __init__(self, matrix, label=None):
        """A 2d linear transformation represented as a matrix. 'matrix' should be something like [[a, b], [c, d]] where a,b,c and d are some numbers."""
        super().__init__()
        self._matrix = np.array(matrix)
        self._label = label
        self._ihat = Vector(self.a, self.c, label="i")
        self._jhat = Vector(self.b, self.d, label="j")
        self._ihat.draw_label_at_end = True
        self._jhat.draw_label_at_end = True
        # self._jhat.label_size = 6
        # self._ihat.label_size = 6

    def copy(self):
        return LinearT(self._matrix)

    @property
    def a(self):
        return self._matrix[0][0]

    @property
    def b(self):
        return self._matrix[0][1]

    @property
    def c(self):
        return self._matrix[1][0]

    @property
    def d(self):
        return self._matrix[1][1]

    @property
    def ihat(self):
        return self._ihat

    @property
    def jhat(self):
        return self._jhat

    def draw(self):
        super().draw()
        
        # visualize the coordinate axes of the linear transformation

        start = config.command_interpretter.initial_transform * Vector(0, 0)
        ix = self.a
        iy = self.c
        itransformed = config.command_interpretter.initial_transform * Vector(ix, iy)
        jx = self.b
        jy = self.d
        jtransformed = config.command_interpretter.initial_transform * Vector(jx, jy)

        l1 = self._canvas.create_line(
            start[0], start[1], itransformed[0], itransformed[1], fill=self._color, arrow=tk.LAST,width=self.line_width
        )
        l2 = self._canvas.create_line(
            start[0], start[1], jtransformed[0], jtransformed[1], fill=self._color, arrow=tk.LAST,width=self.line_width
        )
        self._canvas_items.append(l1)
        self._canvas_items.append(l2)

        if self._label is not None:
            t = self._canvas.create_text(
                start[0], start[1], text=self._label, font=LABEL_FONT, fill=self._color
            )
            self._canvas_items.append(t)

    def __mul__(self, other):
        # matrix matrix multiplication (compose transformations)
        if isinstance(other, LinearT):
            return LinearT(self._matrix @ other._matrix)

        # matrix tuple/list multiplication (transform point)
        if isinstance(other, (list, tuple)):
            return self * Vector(other[0], other[1])

        # matrix vector multiplication (transform vector)
        if isinstance(other, Vector):
            return Vector(
                self.a * other.dx + self.b * other.dy,
                self.c * other.dx + self.d * other.dy,
            )

        # matrix point multiplication (transform point)
        if isinstance(other, Point):
            return Point(
                self.a * other.x + self.b * other.y,
                self.c * other.x + self.d * other.y,
            )

        # matrix polygon multiplication (transform polygon)
        if isinstance(other, Polygon):
            return Polygon([self * p for p in other.points])

        # matrix polyline multiplication (transform polyline)
        if isinstance(other, Polyline):
            return Polyline([self * p for p in other.points])

        return NotImplemented

    def __matmul__(self, other):
        # matrix multiplication
        if isinstance(other, LinearT):
            return LinearT(self._matrix @ other._matrix)

        return NotImplemented

    def __pow__(self, power):
        # matrix power (including negative powers (i.e. inversion))
        # positive power = repeated matrix multiplication
        if isinstance(power, int):
            return LinearT(self._matrix**power)

        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, LinearT):
            return np.array_equal(self._matrix, other._matrix)

        return NotImplemented