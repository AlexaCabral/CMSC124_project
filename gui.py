import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, ttk
import os

def file_directory_description():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = os.path.basename(file_path)
        file_directory_btn.set(file_name)
    else:
        file_directory_btn.set("(None)")



# Main Window
root = tk.Tk()
root.title("LOLCode Interpreter - CMSC 124 Project")
root.geometry("1920x1080+0+0")
root.option_add("*tearOff", False)

# Style
style = ttk.Style(root)

# Import the tcl file
root.tk.call("source", r"C:\Users\asus\Desktop\UP\3rd Year 1st Sem\CMSC 124\project\repo\CMSC124_project\Forest-ttk-theme\forest-dark.tcl")
# Set the theme with the theme_use method
style.theme_use("forest-dark")


# Open file button
file_directory_btn = tk.StringVar(value="(None)")
input_file_btn = tk.Button(
    root, 
    textvariable=file_directory_btn, 
    command=file_directory_description,
    bd=1, 
    relief="ridge"
)
input_file_btn.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
        
        

root.mainloop()