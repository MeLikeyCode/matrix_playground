import tkinter as tk
import numpy as np
import config

from vector import Vector
from point import Point
from polyline import Polyline
from polygon import Polygon
from lineart import LinearT
from affinet import AffineT

from utilities import *


class CommandInterpretter:
    """Runs commands, keeps track of variables, allows manipulation of variables, etc."""

    def __init__(self, canvas: tk.Canvas):
        """'canvas' is the canvas that will be drawn on."""
        self._canvas = canvas
        config.command_interpretter = self
        self._globals = {}
        self._grid_size = 30
        self._grid_offset = self._grid_size * 10
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
        self._canvas.delete(tk.ALL)
        self.draw_grid()
        self.execute_commands_immediate(text)

    def execute_commands_immediate(self, text):
        """Runs the given text as Python code. Does not clear the variables first."""
        exec("from commandinterpretter import *", self._globals)
        exec(text, self._globals)
