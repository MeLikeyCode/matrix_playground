import config
import tkinter as tk
import random
from utilities import random_color

class MathObject:
    """A mathematical object that can be visualized."""

    def __init__(self):
        self._label = None  # label of the object (e.g. "A") on the canvas
        self._canvas: tk.Canvas = (
            config.command_interpretter._canvas  # the canvas the object will be drawn on
        )
        self._canvas_items = (
            []
        )  # the items that are drawn on the canvas to represent this render object (e.g. lines, text, etc.), IMPORTANT: all MathObjects must put all their canvas items in this list
        self._color = random_color()  # color of the object


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
