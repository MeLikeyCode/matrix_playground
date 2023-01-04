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

        command_gui = CodeEditor(self.pane)
        canvas = tk.Canvas(self.pane)

        render_area = CommandInterpretter(canvas)

        self.pane.add(command_gui, width=500)
        self.pane.add(canvas)

        # callbacks
        command_gui.on_execute_script = lambda text: render_area.execute_script(text)
        command_gui.on_run_immediate = lambda text: render_area.execute_commands_immediate(text)

