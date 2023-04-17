import tkinter as tk
from tkinter import ttk

from quickreference import QuickReference
from examples import Examples

class Help(ttk.Frame):
    """Represents the help pane."""

    def __init__(self, master=None):
        super().__init__(master)

        self.create_widgets()

    def create_widgets(self):
        """Creates the widgets of the help pane."""

        self._notebook = ttk.Notebook(self)
        self._notebook.pack(fill=tk.BOTH, expand=True)

        self._quick_reference = QuickReference(self._notebook)
        self._examples = Examples(self._notebook)
        
        self._notebook.add(self._quick_reference, text="Quick Reference")
        self._notebook.add(self._examples, text="Examples")