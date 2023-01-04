import tkinter as tk

class CommandGui(tk.Frame):
    """Represents the GUI where the user types commands, presses buttons to run commands, etc. Basically the left side of the main gui."""

    def __init__(self, master=None):
        super().__init__(master)

        self._shift_button_pressed = False

        self.create_widgets()

    def create_widgets(self):
        self.text = tk.Text(self)
        self.text.insert(tk.END, "Hello World")

        self.button = tk.Button(self,text="Run (shift + enter)", command=self._on_run_button_clicked)

        self.text.pack(fill=tk.BOTH, expand=True)
        self.button.pack()

        # events
        self.text.bind("<Shift_L>", self._on_shift_key_pressed)
        self.text.bind("<Return>", self._on_return_key_pressed)
        self.text.bind("<KeyRelease-Shift_L>", self._on_shift_key_released)

    def _on_run_button_clicked(self):
        print("_on_run_button_clicked executed")

    def _on_shift_key_pressed(self, event):
        print("_on_shift executed")
        self._shift_button_pressed = True

    def _on_return_key_pressed(self, event):
        print("_on_return_key_pressed executed")
        if self._shift_button_pressed:
            self._on_run_button_clicked() # clicking shift + enter is equivalent to clicking the run button
            return "break" # prevent the event from propagating (i.e. "handled")

    def _on_shift_key_released(self, event):
        print("_on_shift_key_released executed")
        self._shift_button_pressed = False