import tkinter as tk
from gui import GUI

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1380x720")
    root.title("Matrix Playground")
    root.iconbitmap("icon.ico")

    gui = GUI(root)
    gui.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
