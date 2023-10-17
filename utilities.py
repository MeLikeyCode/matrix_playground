import random
import numpy as np

def degrees(radians):
    """Converts radians to degrees."""
    return radians * 180 / np.pi

def radians(degrees):
    """Converts degrees to radians."""
    return degrees * np.pi / 180

def random_color():
    """Returns a random color."""
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

class _Options:
    def __init__(self):
        import config
        self._command_interpretter = config.command_interpretter

        self._grid_visible = True

    @property
    def grid(self):
        return self._grid_visible
    
    @grid.setter
    def grid(self, value):
        self._grid_visible = value
        self._command_interpretter.show_grid = value

options = _Options()
