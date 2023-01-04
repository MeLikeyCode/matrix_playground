import tkinter as tk
from gui import GUI

if __name__ == "__main__":
    root = tk.Tk()

    gui = GUI(root)
    gui.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
