import tkinter as tk
from jedi import Script
from completions import Completions
import timeit

FONT = ("Consolas", 11)

class CodeEditor(tk.Frame):
    """Represents the GUI where the user types commands, presses buttons to run commands, etc. Basically the left side of the main gui."""

    def __init__(self, master=None):
        super().__init__(master)

        self._shift_button_pressed = False
        self._shift_button_pressed_immediate = False
        self._ctrl_button_pressed = False
        self._shift_button_pressed_immediate = False
        self._jedi_script_cache = {} # cache jedi scripts so we don't have to re-parse the script every time the user presses a key
        self._jedi_script_cache_size = 100 
        self._completions_up = False

        # combine script window text with command interpretter text (to provide it with context)
        with open('commandinterpretter.py', 'r') as f:
            self._command_interpretter_text = f.read()
        self._completion_offset = self._command_interpretter_text.count('\n') + 2 # +2 for two lines that are added

        self.create_widgets()

        self.get_jedi_script() # calling this once here improves speed (first instance of jedi.Script() instantiation is slow, thus we do it during startup as opposed to during first autocomplete request)

    def create_widgets(self):
        pane = tk.PanedWindow(self, orient=tk.VERTICAL, sashrelief=tk.RAISED,sashwidth=10,sashpad=1)
        pane.pack(fill=tk.BOTH, expand=True)

        script_frame = tk.Frame(pane)
        immediate_frame = tk.Frame(pane)

        pane.add(script_frame)
        pane.add(immediate_frame)
        
        self._script_text = tk.Text(script_frame, font=FONT, wrap=tk.NONE)
        self._script_text.pack(fill=tk.BOTH, expand=True)

        initial_text = """# Type script here. Press 'shift + enter' to run.
# Press 'ctrl + space' to show completions.

T = AffineT([[2,-2,3],[2,2,5]])
draw(T)
"""
        self._script_text.insert(tk.END, initial_text)

        self._completions = Completions(script_frame)

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
        self._script_text.bind("<Key>", self._on_key_pressed)
        self._script_text.bind("<Escape>", self._on_escape_pressed)

        self._immediate_text.bind("<Shift_L>", self._on_shift_key_pressed_immediate)
        self._immediate_text.bind("<Return>", self._on_return_key_pressed_immediate)
        self._immediate_text.bind("<KeyRelease-Shift_L>", self._on_shift_key_released_immediate)
        self._immediate_text.bind("<Control_L>", self._on_ctrl_key_pressed_immediate)
        self._immediate_text.bind("<KeyRelease-Control_L>", self._on_ctrl_key_released_immediate)
        self._immediate_text.bind("<Tab>", self._on_tab_pressed_immediate)
        self._immediate_text.bind("<space>", self._on_space_pressed_immediate)

    def show_completions(self):
        """Called when the user presses ctrl + space."""

        jedi_script = self.get_jedi_script()

        # get position of cursor in script window
        line, col = self._script_text.index(tk.INSERT).split(".")
        line = int(line)
        col = int(col)
        self._completions_initial_cursor_pos = (line, col)

        completions = jedi_script.complete(line + self._completion_offset, col)
        completions = [c for c in completions if not c.name.startswith('_')]

        # get completion names
        completion_names = [c.name for c in completions]

        # show completions
        self._completions.set_completions(completion_names)

        # show completions widget at cursor position
        xpos, ypos, w, h = self._script_text.bbox(tk.INSERT)
        self._completions.place_forget()
        self._completions.place(x=xpos, y=ypos+h)
        self._completions_up = True
        self._completions.set_filter('')

    def on_complete_immediate(self, event):
        """Called when the user presses ctrl + space."""
        # TODO implement
        print("on_complete_immediate")

    def _on_escape_pressed(self, event):
        self._completions.place_forget()
        self._completions_up = False

    def _on_key_pressed(self, event):
        # most logic is schedule to be done during idle (gives a chance for the Text widget to handle the key press first)

        # pressing dot triggers auto completion window
        if event.char == '.':
            self.after_idle(self.show_completions)

        # if auto completion window is up, typing filters it
        if self._completions_up:
            if (not event.char.isalnum()) and (event.char != '\x08'): # backspace
                self._completions.place_forget()
                self._completions_up = False
            else:
                self.after_idle(self._filter_completions)

    def _filter_completions(self):
        """Filters the completions window based on the text between the cursor and the dot to the left of it."""
        line,col = self._script_text.index(tk.INSERT).split(".")
        line = int(line)
        col = int(col)
        if line != self._completions_initial_cursor_pos[0] or col < self._completions_initial_cursor_pos[1]:
            self._completions.place_forget()
            self._completions_up = False
            return

        cursor_line = self._script_text.get("insert linestart", "insert")
        dot_location = cursor_line.rfind('.')
        if dot_location != -1:
            filter = cursor_line[dot_location+1:]
        self._completions.set_filter(filter)

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
            self.after_idle(self.show_completions)
            return "break"

    def _on_space_pressed_immediate(self, event):
        if self._ctrl_button_pressed_immediate:
            # TODO show completions for immediate window
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

    def get_jedi_script(self):
        """Effeciently retrieves a jedi Script object for the current text in the script window. Uses a cached version if possible."""

        # get text from script window
        text = self._script_text.get("1.0", tk.END)

        # if the text is cached, return the cached version
        if text in self._jedi_script_cache:
            return self._jedi_script_cache[text]

        # create a new jedi Script object for this text, cache it, and return it
        # if cache is full, remove the oldest entry
        if len(self._jedi_script_cache) >= self._jedi_script_cache_size:
            self._jedi_script_cache.popitem(last=False)
        all_text = f'{self._command_interpretter_text}\n\n{text}'
        jedi_script = Script(all_text)
        self._jedi_script_cache[text] = jedi_script
        return jedi_script