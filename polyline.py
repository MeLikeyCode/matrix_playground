from mathobject import MathObject
import config
from config import LABEL_FONT
from vector import Vector

class Polyline(MathObject):
    """A polyline."""

    def __init__(self, points=None, label=None):
        super().__init__()
        if points is None:
            points = []
        self._points = points
        self._label = label
        self._points_transformed = [config.command_interpretter.initial_transform * Vector(p[0], p[1]) for p in self._points]

    def copy(self):
        return Polyline(self._points)
    
    def add(self, point):
        """Adds a point to the polyline."""
        self._points.append(point)
        self._points_transformed.append(config.command_interpretter.initial_transform * Vector(point[0], point[1]))
        self.redraw()

    def draw(self):
        super().draw()

        self._points_transformed = [config.command_interpretter.initial_transform * Vector(p[0], p[1]) for p in self._points]

        if len(self._points) < 2:
            return
        
        xys = [p for pt in self._points_transformed for p in pt]
        p = self._canvas.create_line(
            *xys,
            fill=self._color,
            width=self.line_width
        )
        self._canvas_items.append(p)

        if self._label is not None:
            text_x = sum([p[0] for p in self._points]) / len(self._points)
            text_y = sum([p[1] for p in self._points]) / len(self._points)
            pt_transformed = config.command_interpretter.initial_transform * Vector(text_x, text_y)
            t = self._canvas.create_text(
                pt_transformed[0],
                pt_transformed[1],
                text=self._label,
                font=LABEL_FONT,
                fill=self._color,
            )
            self._canvas_items.append(t)