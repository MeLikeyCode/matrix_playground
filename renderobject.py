import tkinter as tk

class RenderObject:
    """Something that can be rendered (visualized) on the RenderArea."""
    def __init__(self):
        self.label = None # label of the object (e.g. "A"), can be None
        
    def clear(self):
        """Removes the underlying canvas items for the object."""
        pass # implemented in subclasses

    def draw(self, canvas):
        """Draws the object on the canvas."""
        pass # implemented in subclasses