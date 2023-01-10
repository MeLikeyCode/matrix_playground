import numpy as np
import config
from config import LABEL_FONT
from mathobject import MathObject
import tkinter as tk

class Vector(MathObject):
    """A 2d vector."""

    def __init__(self, dx, dy, label=None):
        super().__init__()
        self._vector = (dx, dy)
        self._label = label
        self.draw_label_at_end = False  # draw the label at end (or mid-point)
        self._magnitude = np.sqrt(dx**2 + dy**2)
        self._angle = np.arctan2(dy, dx)

    def draw(self):
        pt1transformed = config.command_interpretter.initial_transform * Vector(0, 0)
        pt2transformed = config.command_interpretter.initial_transform * Vector(self._vector[0], self._vector[1])
        l = self._canvas.create_line(
            pt1transformed[0],
            pt1transformed[1],
            pt2transformed[0],
            pt2transformed[1],
            arrow=tk.LAST,
            fill=self._color,
        )
        self._canvas_items.append(l)

        if self._label is not None:
            text_x = self._vector[0] if self.draw_label_at_end else self._vector[0] / 2
            text_y = self._vector[1] if self.draw_label_at_end else self._vector[1] / 2
            pt2transformed = config.command_interpretter.initial_transform * Vector(text_x, text_y)
            t = self._canvas.create_text(
                pt2transformed[0],
                pt2transformed[1],
                text=self._label,
                font=LABEL_FONT,
                fill=self._color,
            )
            self._canvas_items.append(t)

    @property
    def dx(self):
        return self._vector[0]

    @property
    def dy(self):
        return self._vector[1]

    @property
    def magnitude(self):
        return self._magnitude

    @property
    def angle(self):
        return np.degrees(self._angle)

    def copy(self):
        return Vector(self._vector[0], self._vector[1])

    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(
                self._vector[0] + other._vector[0], self._vector[1] + other._vector[1]
            )

        if isinstance(other, Point):
            return Point(
                self._vector[0] + other._point[0], self._vector[1] + other._point[1]
            )

        return NotImplemented

    def __neg__(self):
        return Vector(-self._vector[0], -self._vector[1])

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Vector(self._vector[0] * other, self._vector[1] * other)

        return NotImplemented

    def dot(self, other):
        if not isinstance(other, Vector):
            raise TypeError(
                "dot product can only be computed between two vectors (i.e. 'other' must be a Vector)"
            )

        return self._vector[0] * other._vector[0] + self._vector[1] * other._vector[1]

    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False

        return self._vector == other._vector

    def __getitem__(self, key):
        return self._vector[key]

from point import Point