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
        self._drawn = False # whether a draw() call has been made for this object
        self._line_width = 2 # width of lines drawn for this object


    def clear(self):
        """Clear (erase) the object from the canvas."""
        # Remove the object's canvas items
        for item in self._canvas_items:
            self._canvas.delete(item)
        self._canvas_items = []
        self._drawn = False

    def draw(self):
        """Draws the object on the canvas. 
        
        Must be implemented by subclasses, and subclasses must call super().draw() at the start of their implementation."""
        self._drawn = True

    def _redraw(self):
        """Clears then re-draws the object."""
        if self._drawn:
            self.clear()
            self.draw()

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        self._redraw()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self._redraw()

    @property
    def line_width(self):
        return self._line_width
    
    @line_width.setter
    def line_width(self, value):
        self._line_width = value
        self._redraw()
