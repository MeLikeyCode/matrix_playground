import tkinter as tk
from jedi import Script

FONT = ("Consolas", 11)

class CodeEditor(tk.Frame):
    """Represents the GUI where the user types commands, presses buttons to run commands, etc. Basically the left side of the main gui."""

    def __init__(self, master=None):
        super().__init__(master)

        self._shift_button_pressed = False
        self._shift_button_pressed_immediate = False
        self._ctrl_button_pressed = False
        self._shift_button_pressed_immediate = False

        self.create_widgets()

    def create_widgets(self):
        pane = tk.PanedWindow(self, orient=tk.VERTICAL, sashrelief=tk.RAISED,sashwidth=10,sashpad=1)
        pane.pack(fill=tk.BOTH, expand=True)

        script_frame = tk.Frame(pane)
        immediate_frame = tk.Frame(pane)

        pane.add(script_frame)
        pane.add(immediate_frame)
        
        self._script_text = tk.Text(script_frame, font=FONT, wrap=tk.NONE)
        initial_text = """# Type script here. Press 'shift + enter' to run.

T = AffineT([[2,-2,3],[2,2,5]])
draw(T)
"""
        self._script_text.insert(tk.END, initial_text)

        self._script_text.pack(fill=tk.BOTH, expand=True)

        self._immediate_text = tk.Text(immediate_frame, font=FONT, wrap=tk.NONE)
        self._immediate_text.pack(fill=tk.BOTH, expand=True)

        immediate_initial_text = """# Type code to execute *immediately*
# (i.e. in the current context)
# Press 'shift + enter' to run.

a.color = 'red'"""
        self._immediate_text.insert(tk.END, immediate_initial_text)

        # events
        self._script_text.bind("<Shift_L>", self._on_shift_key_pressed)
        self._script_text.bind("<Return>", self._on_return_key_pressed)
        self._script_text.bind("<KeyRelease-Shift_L>", self._on_shift_key_released)
        self._script_text.bind("<Control_L>", self._on_ctrl_key_pressed)
        self._script_text.bind("<KeyRelease-Control_L>", self._on_ctrl_key_released)
        self._script_text.bind("<Tab>", self._on_tab_pressed)
        self._script_text.bind("<space>", self._on_space_pressed)

        self._immediate_text.bind("<Shift_L>", self._on_shift_key_pressed_immediate)
        self._immediate_text.bind("<Return>", self._on_return_key_pressed_immediate)
        self._immediate_text.bind("<KeyRelease-Shift_L>", self._on_shift_key_released_immediate)
        self._immediate_text.bind("<Control_L>", self._on_ctrl_key_pressed_immediate)
        self._immediate_text.bind("<KeyRelease-Control_L>", self._on_ctrl_key_released_immediate)
        self._immediate_text.bind("<Tab>", self._on_tab_pressed_immediate)
        self._immediate_text.bind("<space>", self._on_space_pressed_immediate)

        self.bind("<<Complete>>", self.on_complete)
        self.bind("<<CompleteImmediate>>", self.on_complete_immediate)

    def on_complete(self, event):
        """Called when the user presses ctrl + space."""

        # get position of cursor in script window
        line, col = self._script_text.index(tk.INSERT).split(".")
        line = int(line)
        col = int(col)

        # get script text
        text = self._script_text.get("1.0", tk.END)

        # combine script text with command interpretter text
        with open('commandinterpretter.py', 'r') as f:
            command_interpretter_text = f.read()

        all_text = command_interpretter_text + '\n\n' + text

        # get completions from combined text (602 is to offset the command interpretter text)
        script = Script(all_text)
        completions = script.complete(line + 602, col)
        print(completions)


    def on_complete_immediate(self, event):
        """Called when the user presses ctrl + space."""
        print("on_complete_immediate")

    def _on_ctrl_key_pressed(self, event):
        self._ctrl_button_pressed = True

    def _on_ctrl_key_released(self, event):
        self._ctrl_button_pressed = False

    def _on_ctrl_key_pressed_immediate(self, event):
        self._ctrl_button_pressed_immediate = True

    def _on_ctrl_key_released_immediate(self, event):
        self._ctrl_button_pressed_immediate = False

    def _on_tab_pressed(self, event):
            # return "break"
            pass

    def _on_tab_pressed_immediate(self, event):
        if self._ctrl_button_pressed_immediate:
            # return "break"
            pass

    def _on_space_pressed(self, event):
        if self._ctrl_button_pressed:
            self.event_generate("<<Complete>>")
            return "break"

    def _on_space_pressed_immediate(self, event):
        if self._ctrl_button_pressed_immediate:
            self.event_generate("<<CompleteImmediate>>")
            return "break"

    def _on_shift_key_pressed_immediate(self, event):
        self._shift_button_pressed_immediate = True

    def _on_return_key_pressed_immediate(self, event):
        if self._shift_button_pressed_immediate:
            the_text = self._immediate_text.get("1.0", tk.END)
            self.on_run_immediate(the_text)
            return "break"

    def _on_shift_key_released_immediate(self, event):
        self._shift_button_pressed_immediate = False

    def _on_shift_key_pressed(self, event):
        self._shift_button_pressed = True

    def _on_return_key_pressed(self, event):
        if self._shift_button_pressed:
            the_text = self._script_text.get("1.0", tk.END)
            self.on_execute_script(the_text)
            return "break" # prevent the event from propagating (i.e. "handled")

    def _on_shift_key_released(self, event):
        self._shift_button_pressed = False

    def on_execute_script(self, text):
        """Called when the user presses the run button or shift + enter in the script window."""
        pass # callback for client

    def on_run_immediate(self, text):
        """Called when the user presses shift + enter in the immediate text box."""
        pass