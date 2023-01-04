import tkinter as tk
import random

render_canvas = None

LABEL_FONT = ("Arial", "20", "bold")


def random_color():
    """Returns a random color in the form of a hex string (e.g. "#ff0000")."""
    return "#%02x%02x%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


class MathObject:
    """A mathematical object that can be rendered on a canvas.

    IMPORTANT: All derived classes must call their draw() method somewhere in their __init__() method.
    This makes it so that the object is drawn as soon as it is created.
    """

    def __init__(self, label="unnamed"):
        self._label = label  # label of the object (e.g. "A") on the canvas
        global render_canvas
        self._canvas: tk.Canvas = (
            render_canvas  # the canvas the object will be drawn on
        )
        self._canvas_items = (
            []
        )  # the items that are drawn on the canvas to represent this render object (e.g. lines, text, etc.)
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
    def __init__(self, dx, dy, label="v"):
        super().__init__()
        self._vector = (dx, dy)
        self._label = label
        self.draw()

    def draw(self):
        l = self._canvas.create_line(
            0, 0, self._vector[0], self._vector[1], arrow=tk.LAST, fill=self._color
        )
        self._canvas_items.append(l)

        text_x = self._vector[0] / 2
        text_y = self._vector[1] / 2
        t = self._canvas.create_text(
            text_x, text_y, text=self._label, font=LABEL_FONT, fill=self._color
        )
        self._canvas_items.append(t)


class Point(MathObject):
    def __init__(self, x, y, label="p"):
        super().__init__()
        self._point = (x, y)
        self._label = label
        self.draw()

    def draw(self):
        o = self._canvas.create_oval(
            self._point[0] - 5,
            self._point[1] - 5,
            self._point[0] + 5,
            self._point[1] + 5,
            fill=self._color,
        )
        self._canvas_items.append(o)

        t = self._canvas.create_text(
            self._point[0],
            self._point[1],
            text=self._label,
            font=LABEL_FONT,
            fill=self._color,
        )
        self._canvas_items.append(t)


class Polyline(MathObject):
    def __init__(self, points, label="p"):
        super().__init__()
        self._points = points
        self._label = label
        self.draw()

    def draw(self):
        p = self._canvas.create_line(*self._points, fill=self._color)
        self._canvas_items.append(p)

        text_x = sum([p[0] for p in self._points]) / len(self._points)
        text_y = sum([p[1] for p in self._points]) / len(self._points)
        t = self._canvas.create_text(
            text_x, text_y, text=self._label, font=LABEL_FONT, fill=self._color
        )
        self._canvas_items.append(t)


class Polygon(MathObject):
    def __init__(self, points, label="p"):
        super().__init__()
        self._points = points
        self._label = label
        self.draw()

    def draw(self):
        p = self._canvas.create_polygon(*self._points, fill=self._color)
        self._canvas_items.append(p)

        text_x = sum([p[0] for p in self._points]) / len(self._points)
        text_y = sum([p[1] for p in self._points]) / len(self._points)
        t = self._canvas.create_text(
            text_x, text_y, text=self._label, font=LABEL_FONT, fill=self._color
        )
        self._canvas_items.append(t)

class Matrix(MathObject):
    def __init__(self, matrix, label="M"):
        super().__init__()
        self._matrix = matrix
        self._label = label
        self.draw()

    def draw(self):
        pass


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
