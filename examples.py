import tkinter as tk

class Examples(tk.Frame):
    """Widget that displays examples.txt."""

    def __init__(self, master=None):
        super().__init__(master)

        self.create_widgets()

    def create_widgets(self):
        """Creates the widgets of the examples pane."""

        self.text = tk.Text(self, wrap=tk.NONE)

        initial_text = """\
Examples
========

"""
        self.text.insert(tk.END, initial_text)
        with open("examples.txt", "r") as f:
            self.text.insert(tk.END, f.read())

        # create a vertical scrollbar
        self.vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.text.config(yscrollcommand=self.vscrollbar.set)

        # create a horizontal scrollbar
        self.hscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL, command=self.text.xview)
        self.text.config(xscrollcommand=self.hscrollbar.set)

        self.vscrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.hscrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.text.config(state=tk.DISABLED)
        self.text.config(font=("consolas", 12))
        self.text.config(bg="#ffffe0") # yellowish paper-colored background color