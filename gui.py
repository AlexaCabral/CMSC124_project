import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, ttk, scrolledtext
import os

def openFile():
    file_path = filedialog.askopenfilename()
    if file_path:
        base_name = os.path.basename(file_path)
        file_name.set(base_name)
        
        file = open(file_path, "r")
        content = file.read()
        text_editor.delete("1.0", "end")
        text_editor.insert("1.0", content)
    
        file.close()
    else:
        file_name.set("(None) - Open a File")



# Main Window
root = tk.Tk()
root.title("LOLCode Interpreter - CMSC 124 Project")
root.geometry("1920x1080+-5+0")
root.option_add("*tearOff", False)

# Style
style = ttk.Style(root)

# Import the tcl file
root.tk.call("source", r"C:\Users\asus\Desktop\UP\3rd Year 1st Sem\CMSC 124\project\repo\CMSC124_project\Forest-ttk-theme\forest-dark.tcl")
# Set the theme with the theme_use method
style.theme_use("forest-dark")


# File Explorer - Text Editor
file_name = tk.StringVar(value="(None) - Open a File")
file_explorer_button = ttk.Button(root, textvariable=file_name, command=openFile, style="Accent.TButton")
file_explorer_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

text_editor = scrolledtext.ScrolledText(root, width=75, height=25, fg='white', bg="#404040")
text_editor.grid(row=1, column=0, padx=5, pady=5, rowspan=2, sticky="nsew")

root.mainloop()