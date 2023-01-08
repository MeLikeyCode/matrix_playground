import tkinter as tk
import typing

class Completions(tk.Frame):
    """Auto-completion/call hint widget."""

    def __init__(self, master=None):
        super().__init__(master)

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
        self._listbox.delete(0, tk.END)
        for completion in completions:
            self._listbox.insert(tk.END, completion)



    