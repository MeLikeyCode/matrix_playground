import tkinter as tk
from codeeditor import CodeEditor
from commandinterpretter import CommandInterpretter

class GUI(tk.Frame):
    """Represents the GUI of the application as a whole."""

    def __init__(self, master=None):
        super().__init__(master)
        
        self._shift_button_pressed = False

        self.create_widgets()

    def create_widgets(self):
        """Creates the widgets of the GUI."""
        self.pane = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashrelief=tk.RAISED,sashwidth=10,sashpad=1)
        self.pane.pack(fill=tk.BOTH, expand=True)

        code_editor = CodeEditor(self.pane)
        canvas = tk.Canvas(self.pane)

        command_interpretter = CommandInterpretter(canvas)

        self.pane.add(code_editor, width=500)
        self.pane.add(canvas)

        # callbacks
        code_editor.on_execute_script = lambda text: command_interpretter.execute_script(text)
        code_editor.on_run_immediate = lambda text: command_interpretter.execute_commands_immediate(text)

