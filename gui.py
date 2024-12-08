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

def execute():
    for item in lexemes_treeview.get_children():
        lexemes_treeview.delete(item)

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

# List of Tokens -  Symbol Table
header = tk.Label(root, text="LOL CODE Interpreter", font=("Helvetica", 12, "bold"))
header.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# (3) List of Tokens
lexemes_header = tk.Label(root, text="Lexemes", font=("Helvetica", 12), relief="ridge")
lexemes_header.grid(row=1, column=1, padx=5, pady=5, sticky='NSEW')

lexemes_treeview = ttk.Treeview(root, selectmode="browse", columns=(1, 2), height=20)
lexemes_treeview.grid(row=2, column=1, padx=5, pady=5)
# Column
lexemes_treeview.column("#0", width=0, stretch=False)
lexemes_treeview.column(1, anchor="w", width=220)
lexemes_treeview.column(2, anchor="w", width=220)
# Headings
lexemes_treeview.heading("#0", text="", anchor="w")
lexemes_treeview.heading(1, text=" Lexeme", anchor="w")
lexemes_treeview.heading(2, text=" Classification", anchor="w")

# (4) Symbol Table
symbol_header = tk.Label(root, text="Symbol Table", font=("Helvetica", 12), relief="ridge")
symbol_header.grid(row=1, column=2, padx=5, pady=5, sticky='NSEW')

symbol_treeview = ttk.Treeview(root, selectmode="browse", columns=(1, 2), height=20)
symbol_treeview.grid(row=2, column=2, padx=5, pady=5)
# Column
symbol_treeview.column("#0", width=0, stretch=False)
symbol_treeview.column(1, anchor="w", width=220)
symbol_treeview.column(2, anchor="w", width=220)
# Headings
symbol_treeview.heading("#0", text="", anchor="w")
symbol_treeview.heading(1, text=" Identifier", anchor="w")
symbol_treeview.heading(2, text=" Value", anchor="w")


# Dummy data to visualize treeview
dummy_data = [
    ("HAI", "Code Delimiter"),
    ("KTHXBYE", "End of Program"),
    ("VISIBLE", "Output Statement"),
    ("GIMMEH", "Input Statement"),
    ("I HAS A", "Variable Declaration"),
    ("ITZ", "Variable Initialization"),
    ("SUM OF", "Addition Operation"),
    ("DIFF OF", "Subtraction Operation"),
    ("PRODUKT OF", "Multiplication Operation"),
    ("QUOSHUNT OF", "Division Operation"),
]

dummy_data_symbol = [
    ("IT", "noot noot 12"),
    ("var", "12"),
]

for keyword, classification in dummy_data:
    lexemes_treeview.insert("", "end", values=(keyword, classification))
    
for identifier, value in dummy_data_symbol:
    symbol_treeview.insert("", "end", values=(identifier, value))
    
# Execution/Run Button - Console
execute_button = ttk.Button(root, text="Execute", style="Accent.TButton", command=execute)
execute_button.grid(row=3, column=0, padx=5, pady=5, sticky="nsew", columnspan=3)

console = scrolledtext.ScrolledText(root, height=20, font=("Helvetica", 12), fg='white', bg="#404040")
console.grid(row=4, column=0, padx=5, pady=5, sticky="nsew", columnspan=3)

root.mainloop()