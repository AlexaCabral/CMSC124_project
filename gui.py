import tkinter as tk
from tkinter import filedialog, messagebox


class LOLCodeGUI:
     def __init__(self, root):
        self.root = root
        self.root.title("LOLCode Interpreter - CMSC 124 Project")
        self.root.geometry("1920x1080+0+0")
        self.root.configure(bg="gray")



root = tk.Tk()
app = LOLCodeGUI(root)
root.mainloop()