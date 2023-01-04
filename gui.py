import tkinter as tk
from commandgui import CommandGui
from renderarea import RenderArea
from vectorobject import VectorObject

class GUI(tk.Frame):
    """Represents the GUI of the application as a whole."""

    def __init__(self, master=None):
        super().__init__(master)
        
        self._shift_button_pressed = False

        self.create_widgets()

    def create_widgets(self):
        """Creates the widgets of the GUI."""
        self.pane = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
        self.pane.pack(fill=tk.BOTH, expand=True)

        command_gui = CommandGui(self.pane)
        self.canvas = tk.Canvas(self.pane)

        render_area = RenderArea(self.canvas)
        render_area.add_object(VectorObject())

        self.pane.add(command_gui, width=400)
        self.pane.add(self.canvas)

