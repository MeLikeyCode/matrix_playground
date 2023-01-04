import tkinter as tk

class RenderArea:
    """Represents the area where matrices/vectors are rendered (visualized). Basically, the right side of the application."""

    def __init__(self, canvas: tk.Canvas):
        """'canvas' is the canvas that will be drawn on."""
        self._render_objects = [] # objects to draw (matrices/vectors)
        self._canvas = canvas

    def add_object(self, obj):
        self._render_objects.append(obj)
        obj._canvas = self._canvas
        obj.draw()

    def remove_object(self, obj):
        obj.clear()
        self._render_objects.remove(obj)




