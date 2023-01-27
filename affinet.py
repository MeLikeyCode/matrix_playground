from mathobject import MathObject
import config
from config import LABEL_FONT
from vector import Vector
from point import Point
from lineart import LinearT
import numpy as np
import tkinter as tk
from polyline import Polyline
from polygon import Polygon

class AffineT(MathObject):
    @staticmethod
    def identity():
        return AffineT([[1, 0, 0], [0, 1, 0]])

    @staticmethod
    def translation(tx, ty):
        return AffineT([[1, 0, tx], [0, 1, ty]])

    @staticmethod
    def rotation(angle):
        angle = np.radians(angle)
        return AffineT([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0]])

    @staticmethod
    def scaling(sx, sy):
        return AffineT([[sx, 0, 0], [0, sy, 0]])

    def __init__(self, matrix, label=None):
        """An 2d affine transformation represented as a matrix. 'matrix' should be something like [[a, b, c], [d, e, f]] where a,b,c,d,e and f are some numbers.

        The actual matrix that will be constructed will be:
        [a, b, c] where c and f are the tx ty components, a, e are the scale components, b d are shear components, and a b, d e are the rotation components.
        [d, e, f]
        [0, 0, 1]
        """
        super().__init__()
        self._matrix = np.array([matrix[0], matrix[1], [0, 0, 1]])
        self._label = label
        self._linear = LinearT(self._matrix[:2, :2])
        self._translation = Vector(self._matrix[0][2], self._matrix[1][2])

    def copy(self):
        return AffineT(self._matrix)

    @property
    def a(self):
        return self._matrix[0][0]

    @property
    def b(self):
        return self._matrix[0][1]

    @property
    def c(self):
        return self._matrix[0][2]

    @property
    def d(self):
        return self._matrix[1][0]

    @property
    def e(self):
        return self._matrix[1][1]

    @property
    def f(self):
        return self._matrix[1][2]

    @property
    def ihat(self):
        return self._linear.ihat

    @property
    def jhat(self):
        return self._linear.jhat

    @property
    def linear(self):
        """The linear transformation component of the affine transformation (i.e. excludes the translation)."""
        return self._linear

    @property
    def tx(self):
        return self._matrix[0][2]

    @property
    def ty(self):
        return self._matrix[1][2]

    def draw(self):
        # visualize the coordinate axes of the affine transformation

        tx = self.c
        ty = self.f
        ttransformed = config.command_interpretter.initial_transform * Vector(tx, ty)

        ix = tx + self.a
        iy = ty + self.d
        itransformed = config.command_interpretter.initial_transform * Vector(ix, iy)
        jx = tx + self.b
        jy = ty + self.e
        jtransformed = config.command_interpretter.initial_transform * Vector(jx, jy)

        l1 = self._canvas.create_line(ttransformed[0], ttransformed[1], itransformed[0], itransformed[1], fill=self._color, arrow=tk.LAST)
        l2 = self._canvas.create_line(ttransformed[0], ttransformed[1], jtransformed[0], jtransformed[1], fill=self._color, arrow=tk.LAST)
        self._canvas_items.append(l1)
        self._canvas_items.append(l2)
        i1 = self._canvas.create_text(
            itransformed[0], itransformed[1], text="i", font=LABEL_FONT, fill=self._color
        )
        i2 = self._canvas.create_text(
            jtransformed[0], jtransformed[1], text="j", font=LABEL_FONT, fill=self._color
        )
        self._canvas_items.append(i1)
        self._canvas_items.append(i2)

        if self._label is not None:
            t = self._canvas.create_text(
                ttransformed[0],
                ttransformed[1],
                text=self._label,
                font=LABEL_FONT,
                fill=self._color,
            )
            self._canvas_items.append(t)

    def __mul__(self, other):
        # matrix matrix multiplication (compose transformations)
        if isinstance(other, AffineT):
            return AffineT(self._matrix @ other._matrix)

        # matrix list/tuple multiplication (transform list/tuple of points)
        if isinstance(other, (list, tuple)):
            return self * Vector(other[0], other[1])

        # matrix vector multiplication (transform vector)
        if isinstance(other, Vector):
            return Vector(
                self.a * other.dx + self.b * other.dy + self.c,
                self.d * other.dx + self.e * other.dy + self.f,
            )

        # matrix point multiplication (transform point)
        if isinstance(other, Point):
            return Point(
                self.a * other.x + self.b * other.y + self.c,
                self.d * other.x + self.e * other.y + self.f,
            )

        # matrix polygon multiplication (transform polygon)
        if isinstance(other, Polygon):
            return Polygon([self * point for point in other._points])

        # matrix polyline multiplication (transform polyline)
        if isinstance(other, Polyline):
            return Polyline([self * point for point in other._points])

        return NotImplemented

    def __matmul__(self, other):
        # matrix multiplication
        if isinstance(other, AffineT):
            return AffineT(self._matrix @ other._matrix)

        return NotImplemented

    def __pow__(self, power):
        # invert the matrix, e.g. M**-1 (only accepts -1 as the power)
        if isinstance(power, int) and power == -1:
            return AffineT(np.linalg.inv(self._matrix))

        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, AffineT):
            return np.array_equal(self._matrix, other._matrix)

        return NotImplemented