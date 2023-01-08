import tkinter as tk
import typing

class Completions(tk.Frame):
    """Auto-completion/call hint widget."""

    def __init__(self, master=None):
        super().__init__(master)

        self._completions = []
        self._filter = ''
        scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self._listbox = tk.Listbox(self, yscrollcommand=scrollbar.set)
        scrollbar.config(command=self._listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def _on_return_key_pressed(self, event):
        self.on_completion_selected()

    def on_completion_selected(self):
        """Called when a completion is selected."""
        pass # assignable callback

    def set_completions(self, completions: typing.Collection[str]):
        """Set the completions to display."""
        self._completions = completions
        self._draw()

    def _draw(self):
        self._listbox.delete(0, tk.END)
        matching = [completion for completion in self._completions if completion.startswith(self._filter)]
        for completion in matching:
            self._listbox.insert(tk.END, completion)

    def set_filter(self, filter: str):
        """Set the filter to use when displaying completions."""
        self._filter = filter
        self._draw()



    