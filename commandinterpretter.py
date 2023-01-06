import tkinter as tk
import random
import numpy as np


LABEL_FONT = ("Arial", "20", "bold")

command_interpretter = None


def random_color():
    """Returns a random color in the form of a hex string (e.g. "#ff0000")."""
    return "#%02x%02x%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def draw(*objects):
    """Draws the given MathObjects."""
    for obj in objects:
        obj.draw()


def clear(*objects):
    """Clears the given MathObjects from the canvas."""
    for obj in objects:
        obj.clear()


class MathObject:
    """A mathematical object that can be rendered on a canvas."""

    def __init__(self):
        self._label = None  # label of the object (e.g. "A") on the canvas
        self._canvas: tk.Canvas = (
            command_interpretter._canvas  # the canvas the object will be drawn on
        )
        self._canvas_items = (
            []
        )  # the items that are drawn on the canvas to represent this render object (e.g. lines, text, etc.), IMPORTANT: all MathObjects must put all their canvas items in this list
        self._color = random_color()  # color of the object

    def __del__(self):
        self.clear()

    def clear(self):
        """Clear (erase) the object from the canvas."""
        # Remove the object's canvas items
        for item in self._canvas_items:
            self._canvas.delete(item)
        self._canvas_items = []

    def draw(self):
        """Draws the object on the canvas."""
        raise NotImplementedError()  # implemented in subclasses (add items to self._canvas_items)

    def redraw(self):
        """Clears then re-draws."""
        self.clear()
        self.draw()

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        self.redraw()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self.redraw()


class Vector(MathObject):
    def __init__(self, dx, dy, label=None):
        super().__init__()
        self._vector = (dx, dy)
        self._label = label
        self.draw_label_at_end = False  # draw the label at end (or mid-point)
        self._magnitude = np.sqrt(dx**2 + dy**2)
        self._angle = np.arctan2(dy, dx)

    def draw(self):
        pt1transformed = command_interpretter.initial_transform * Vector(0, 0)
        pt2transformed = command_interpretter.initial_transform * Vector(self._vector[0], self._vector[1])
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
            pt2transformed = command_interpretter.initial_transform * Vector(text_x, text_y)
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
        return self._angle

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


class Point(MathObject):
    def __init__(self, x, y, label=None):
        super().__init__()
        self._point = (x, y)
        self._label = label

    def draw(self):
        transformed = command_interpretter.initial_transform * Vector(self._point[0], self._point[1])
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

    @property
    def x(self):
        return self._point[0]

    @property
    def y(self):
        return self._point[1]

    def __getitem__(self, key):
        return self._point[key]


class Polyline(MathObject):
    def __init__(self, points, label=None):
        super().__init__()
        self._points = points
        self._label = label
        self._points_transformed = [command_interpretter.initial_transform * Vector(p[0], p[1]) for p in points]

    def draw(self):
        xys = [p for pt in self._points_transformed for p in pt]
        p = self._canvas.create_line(
            *xys,
            fill=self._color,
        )
        self._canvas_items.append(p)

        if self._label is not None:
            text_x = sum([p[0] for p in self._points]) / len(self._points)
            text_y = sum([p[1] for p in self._points]) / len(self._points)
            pt_transformed = command_interpretter.initial_transform * Vector(text_x, text_y)
            t = self._canvas.create_text(
                pt_transformed[0],
                pt_transformed[1],
                text=self._label,
                font=LABEL_FONT,
                fill=self._color,
            )
            self._canvas_items.append(t)


class Polygon(MathObject):
    def __init__(self, points, label=None):
        super().__init__()
        self._points = points
        self._label = label
        self._points_transformed = [command_interpretter.initial_transform * Vector(p[0], p[1]) for p in points]

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
            pt_transformed = command_interpretter.initial_transform * Vector(text_x, text_y)
            t = self._canvas.create_text(
                pt_transformed[0],
                pt_transformed[1],
                text=self._label,
                font=LABEL_FONT,
                fill='#fff', # label and polygon have to be different colors
            )
            self._canvas_items.append(t)


class LinearT(MathObject):
    @staticmethod
    def identity():
        return LinearT([[1, 0], [0, 1]])
    
    @staticmethod
    def rotation(angle):
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
        # visualize the coordinate axes of the linear transformation

        ix = self.a
        iy = self.c
        jx = self.b
        jy = self.d

        l1 = self._canvas.create_line(
            0, 0, ix * grid_size, iy * grid_size, fill=self._color, arrow=tk.LAST
        )
        l2 = self._canvas.create_line(
            0, 0, jx * grid_size, jy * grid_size, fill=self._color, arrow=tk.LAST
        )
        self._canvas_items.append(l1)
        self._canvas_items.append(l2)

        if self._label is not None:
            t = self._canvas.create_text(
                0, 0, text=self._label, font=LABEL_FONT, fill=self._color
            )
            self._canvas_items.append(t)

    def __mul__(self, other):
        # matrix vector multiplication
        if isinstance(other, Vector):
            return Vector(
                self.a * other.dx + self.b * other.dy,
                self.c * other.dx + self.d * other.dy,
            )

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


class AffineT(MathObject):
    @staticmethod
    def identity():
        return AffineT([[1, 0, 0], [0, 1, 0]])

    @staticmethod
    def translation(tx, ty):
        return AffineT([[1, 0, tx], [0, 1, ty]])

    @staticmethod
    def rotation(angle):
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

        ix = tx + self.a
        iy = ty + self.d
        jx = tx + self.b
        jy = ty + self.e

        l1 = self._canvas.create_line(
            tx * grid_size,
            ty * grid_size,
            ix * grid_size,
            iy * grid_size,
            fill=self._color,
            arrow=tk.LAST,
        )
        l2 = self._canvas.create_line(
            tx * grid_size,
            ty * grid_size,
            jx * grid_size,
            jy * grid_size,
            fill=self._color,
            arrow=tk.LAST,
        )
        self._canvas_items.append(l1)
        self._canvas_items.append(l2)
        i1 = self._canvas.create_text(
            ix * grid_size, iy * grid_size, text="i", font=LABEL_FONT, fill=self._color
        )
        i2 = self._canvas.create_text(
            jx * grid_size, jy * grid_size, text="j", font=LABEL_FONT, fill=self._color
        )
        self._canvas_items.append(i1)
        self._canvas_items.append(i2)

        if self._label is not None:
            t = self._canvas.create_text(
                tx * grid_size,
                ty * grid_size,
                text=self._label,
                font=LABEL_FONT,
                fill=self._color,
            )
            self._canvas_items.append(t)

    def __mul__(self, other):
        # matrix vector multiplication
        if isinstance(other, Vector):
            return Vector(
                self.a * other.dx + self.b * other.dy + self.c,
                self.d * other.dx + self.e * other.dy + self.f,
            )

        return NotImplemented

    def __matmul__(self, other):
        # matrix multiplication
        if isinstance(other, AffineT):
            return AffineT(self._matrix @ other._matrix)

        return NotImplemented

    def __pow__(self, power):
        # matrix power (including negative powers (i.e. inversion))
        # positive power = repeated matrix multiplication
        if isinstance(power, int):
            return AffineT(self._matrix**power)

        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, AffineT):
            return np.array_equal(self._matrix, other._matrix)

        return NotImplemented


class CommandInterpretter:
    """Runs commands, keeps track of variables, allows manipulation of variables, etc."""

    def __init__(self, canvas: tk.Canvas):
        """'canvas' is the canvas that will be drawn on."""
        self._canvas = canvas
        global command_interpretter
        command_interpretter = self
        self._globals = {}
        self._grid_size = 20
        self._grid_offset = 200
        self._initial_transform = AffineT.identity() @ AffineT.translation(self._grid_offset,self._grid_offset) @ AffineT.scaling(self._grid_size,self._grid_size)

        self._canvas.bind("<Configure>", lambda e: self.draw_grid())

    @property
    def initial_transform(self):
        return self._initial_transform

    def clear_grid(self):
        self._canvas.delete("grid")

    def draw_grid(self):
        self.clear_grid()

        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        for i in range(0, width, self._grid_size):
            self._canvas.create_line(i, 0, i, height, fill="#ddd", tags="grid")
        for i in range(0, height, self._grid_size):
            self._canvas.create_line(0, i, width, i, fill="#ddd", tags="grid")

        # create the origin
        self._canvas.create_line(self._grid_offset, 0, self._grid_offset, height, fill="#666", tags="grid")
        self._canvas.create_line(0, self._grid_offset, width, self._grid_offset, fill="#666", tags="grid")

        self._canvas.tag_lower("grid")

    def execute_script(self, text):
        """Runs the given text as Python code. Clears the variables first."""
        self._globals = {}
        self.execute_commands_immediate(text)

    def execute_commands_immediate(self, text):
        """Runs the given text as Python code. Does not clear the variables first."""
        exec("from commandinterpretter import *", self._globals)
        exec(text, self._globals)
