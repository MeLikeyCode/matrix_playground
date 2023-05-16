import tkinter as tk
import numpy as np
import config
import math
import time

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
        self.math_objects = []
        self._canvas = canvas
        config.command_interpretter = self
        self._globals = {}
        self._grid_size = 30 # equivalent to scale (zoom), in pixels
        self._grid_offset = (
            self._grid_size * 10
        )  # IMPORTANT: must be a multiple of grid_size (maybe can remove this constraint later)
        self._initial_transform = (
            AffineT.identity()
            @ AffineT.translation(self._grid_offset, self._grid_offset)
            @ AffineT.scaling(self._grid_size, self._grid_size)
        )
        self._fps = 30

        self._canvas.bind("<Configure>", lambda e: self.draw_grid())
        
        self._canvas.bind("<ButtonPress-3>", self.scroll_start)
        self._canvas.bind("<ButtonPress-2>", self.scroll_start)
        self._canvas.bind("<B3-Motion>", self.scroll_move)
        self._canvas.bind("<B2-Motion>", self.scroll_move)
        self._canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        self._time_last = time.time()
        self._canvas.after(int(1000/self._fps),self._on_update)

    @property
    def grid_size(self):
        return self._grid_size
    
    @grid_size.setter
    def grid_size(self, value):
        self._grid_size = value
        self._grid_offset = self._grid_size * 10
        self._initial_transform = (
            AffineT.identity()
            @ AffineT.translation(self._grid_offset, self._grid_offset)
            @ AffineT.scaling(self._grid_size, self._grid_size)
        )
        self.redraw()

    @property
    def transform(self):
        """Returns an affine matrix that transforms from canvas space to grid space."""
        return self._initial_transform
    
    def _on_mousewheel(self, event):
        factor = 1.5
        self.grid_size += factor * (event.delta / 120)

    def _on_update(self):
        """Executed roughly every 1/fps seconds."""
        time_now = time.time()
        
        try:
            if "on_update" in self._globals:
                self._globals["on_update"](time_now - self._time_last)
        except Exception as e:
            print("Error in on_update():",e)
        finally:
            self._time_last = time_now
            self._canvas.after(int(1000/self._fps),self._on_update)

    @property
    def initial_transform(self):
        return self._initial_transform

    def scroll_start(self, event):
        self._canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self._canvas.scan_dragto(event.x, event.y, gain=1)
        self.draw_grid()

    def clear_grid(self):
        self._canvas.delete("grid")

    def redraw(self):
        # redraw grid
        self.draw_grid()

        # redraw mathobjects
        for obj in self.math_objects:
            obj.redraw()

    def draw_grid(self):
        self.clear_grid()

        # get area that camera is viewing (only draw grid in this area)
        tl, tr, br, bl = self.camera_rect()

        # round to nearest grid_size
        tl = (round(tl[0] / self._grid_size) * self._grid_size, round(tl[1] / self._grid_size) * self._grid_size)
        tr = (round(tr[0] / self._grid_size) * self._grid_size, round(tr[1] / self._grid_size) * self._grid_size)
        br = (round(br[0] / self._grid_size) * self._grid_size, round(br[1] / self._grid_size) * self._grid_size)
        bl = (round(bl[0] / self._grid_size) * self._grid_size, round(bl[1] / self._grid_size) * self._grid_size)

        # draw grid
        for i in np.arange(tl[0], tr[0], self._grid_size):
            self._canvas.create_line(i, tl[1], i, bl[1], fill="#ddd", tags="grid")
        for i in np.arange(tl[1], bl[1], self._grid_size):
            self._canvas.create_line(tl[0], i, tr[0], i, fill="#ddd", tags="grid")

        # draw origin
        self._canvas.create_line(self._grid_offset, tl[1], self._grid_offset, bl[1], fill="#666", tags="grid")
        self._canvas.create_line(tl[0], self._grid_offset, tr[0], self._grid_offset, fill="#666", tags="grid")

        self._canvas.tag_lower("grid")

    def execute_script(self, text):
        """Runs the given text as Python code. Clears the variables first."""
        self.math_objects.clear()
        self._globals.clear()
        self._canvas.delete(tk.ALL)
        self.draw_grid()
        self.execute_commands_immediate(text)

    def execute_commands_immediate(self, text):
        """Runs the given text as Python code. Does not clear the variables first."""
        exec("from commandinterpretter import *", self._globals)
        exec(text, self._globals)

    def camera_rect(self):
        """Returns a rectangle representing area of the canvas that the camera (window) is currently viewing.

        Returned value is (top_left, top_right, bottom_right, bottom_left), where each point is (x,y) tuple.
        """
        window_width = self._canvas.winfo_width()
        window_height = self._canvas.winfo_height()

        return (
            (self._canvas.canvasx(0), self._canvas.canvasy(0)),
            (self._canvas.canvasx(window_width), self._canvas.canvasy(0)),
            (self._canvas.canvasx(window_width), self._canvas.canvasy(window_height)),
            (self._canvas.canvasx(0), self._canvas.canvasy(window_height)),
        )
