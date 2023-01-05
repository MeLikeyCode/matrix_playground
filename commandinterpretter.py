import tkinter as tk
import random
import numpy as np


render_canvas = None

LABEL_FONT = ("Arial", "20", "bold")


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
        global render_canvas
        self._canvas: tk.Canvas = (
            render_canvas  # the canvas the object will be drawn on
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
        self.draw_label_at_end = False # draw the label at end (or mid-point)

    def draw(self):
        l = self._canvas.create_line(
            0, 0, self._vector[0], self._vector[1], arrow=tk.LAST, fill=self._color
        )
        self._canvas_items.append(l)

        if self._label is not None:
            text_x = self._vector[0] if self.draw_label_at_end else self._vector[0] / 2
            text_y = self._vector[1] if self.draw_label_at_end else self._vector[1] / 2
            t = self._canvas.create_text(
                text_x, text_y, text=self._label, font=LABEL_FONT, fill=self._color
            )
            self._canvas_items.append(t)


class Point(MathObject):
    def __init__(self, x, y, label=None):
        super().__init__()
        self._point = (x, y)
        self._label = label

    def draw(self):
        o = self._canvas.create_oval(
            self._point[0] - 5,
            self._point[1] - 5,
            self._point[0] + 5,
            self._point[1] + 5,
            fill=self._color,
        )
        self._canvas_items.append(o)

        if self._label is not None:
            t = self._canvas.create_text(
                self._point[0],
                self._point[1],
                text=self._label,
                font=LABEL_FONT,
                fill=self._color,
            )
            self._canvas_items.append(t)


class Polyline(MathObject):
    def __init__(self, points, label=None):
        super().__init__()
        self._points = points
        self._label = label

    def draw(self):
        p = self._canvas.create_line(*self._points, fill=self._color)
        self._canvas_items.append(p)

        if self._label is not None:
            text_x = sum([p[0] for p in self._points]) / len(self._points)
            text_y = sum([p[1] for p in self._points]) / len(self._points)
            t = self._canvas.create_text(
                text_x, text_y, text=self._label, font=LABEL_FONT, fill=self._color
            )
            self._canvas_items.append(t)


class Polygon(MathObject):
    def __init__(self, points, label=None):
        super().__init__()
        self._points = points
        self._label = label

    def draw(self):
        p = self._canvas.create_polygon(*self._points, fill=self._color)
        self._canvas_items.append(p)

        if self._label is not None:
            text_x = sum([p[0] for p in self._points]) / len(self._points)
            text_y = sum([p[1] for p in self._points]) / len(self._points)
            t = self._canvas.create_text(
                text_x, text_y, text=self._label, font=LABEL_FONT, fill=self._color
            )
            self._canvas_items.append(t)

class LinearT(MathObject):
    def __init__(self, matrix, label=None):
        """A 2d linear transformation represented as a matrix. 'matrix' should be something like [[a, b], [c, d]] where a,b,c and d are some numbers."""
        super().__init__()
        self._matrix = np.array(matrix)
        self._label = label
        self._ihat = Vector(self.a, self.c, label="i")
        self._jhat = Vector(self.b, self.d, label="j")
        self._ihat.draw_label_at_end = True
        self._jhat.draw_label_at_end = True

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
        base_length = 100

        ihat = self.ihat
        ihat.color = self._color
        ihat.draw()
        jhat = self.jhat
        jhat.color = self._color
        jhat.draw()

        if self._label is not None:
            self._canvas.create_text(10,10, text=self._label, font=LABEL_FONT, fill=self._color)


class CommandInterpretter:
    """Runs commands, keeps track of variables, allows manipulation of variables, etc."""

    def __init__(self, canvas: tk.Canvas):
        """'canvas' is the canvas that will be drawn on."""
        self._canvas = canvas
        global render_canvas
        render_canvas = self._canvas
        self._globals = {}

    def execute_script(self, text):
        """Runs the given text as Python code. Clears the variables first."""
        self._globals = {}
        self.execute_commands_immediate(text)

    def execute_commands_immediate(self, text):
        """Runs the given text as Python code. Does not clear the variables first."""
        exec('from commandinterpretter import *', self._globals)
        exec(text, self._globals)
