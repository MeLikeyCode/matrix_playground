from renderobject import RenderObject

class VectorObject(RenderObject):
    def __init__(self):
        super().__init__()
        self._vector = (100,100)
        self._draw_as = "vector" # can also be "point"
        self._canvas_items = []

    def clear(self):
        for item in self._canvas_items:
            self._canvas.delete(item)
        self._canvas_items = []

    def draw(self):
        l = self._canvas.create_line(0,0,self._vector[0],self._vector[1])
        self._canvas_items.append(l)

    

