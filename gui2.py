import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, scrolledtext
import os
from interpreter import Interpreter  

file_path = ""  

def openFile():
    global file_path
    file_path = filedialog.askopenfilename()
    if file_path:  
        base_name = os.path.basename(file_path)
        file_name.set(base_name)

        with open(file_path, "r") as file:
            content = file.read()
            text_editor.delete("1.0", "end")
            text_editor.insert("1.0", content)
    else:
        file_name.set("(None) - Open a File")  

def execute():
    global file_path

    if file_path:  
        interpreter = Interpreter(console)

        with open(file_path, 'r') as file:
            code_lines = file.readlines()

        interpreter.process_code(code_lines)

        lexemes = interpreter.get_lexemes()
        variables = interpreter.get_variables()

        for item in lexemes_treeview.get_children():
            lexemes_treeview.delete(item)
        for item in symbol_treeview.get_children():
            symbol_treeview.delete(item)

        for lexeme, classification in lexemes:
            lexemes_treeview.insert("", "end", values=(lexeme, classification))

        for var, value in variables.items():
            symbol_treeview.insert("", "end", values=(var, value))
    else:
        console.insert(tk.END, "No file selected. Please select a file to load first.\n")

root = tk.Tk()
root.title("LOLCode Interpreter - CMSC 124 Project")
root.geometry("1920x1080+-5+0")
root.option_add("*tearOff", False)

style = ttk.Style(root)

root.tk.call("source", r"C:\Users\denal\Desktop\codes\CMSC 124\CMSC124_project\Forest-ttk-theme\forest-dark.tcl")
style.theme_use("forest-dark")

file_name = tk.StringVar(value="(None) - Open a File")
file_explorer_button = ttk.Button(root, textvariable=file_name, command=openFile, style="Accent.TButton")
file_explorer_button.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

text_editor = scrolledtext.ScrolledText(root, width=75, height=25, fg='white', bg="#404040")
text_editor.grid(row=1, column=0, padx=5, pady=5, rowspan=2, sticky="nsew")

header = tk.Label(root, text="LOL CODE Interpreter", font=("Helvetica", 12, "bold"))
header.grid(row=0, column=1, padx=5, pady=5, sticky="w")

lexemes_header = tk.Label(root, text="Lexemes", font=("Helvetica", 12), relief="ridge")
lexemes_header.grid(row=1, column=1, padx=5, pady=5, sticky='NSEW')

lexemes_treeview = ttk.Treeview(root, selectmode="browse", columns=(1, 2), height=20)
lexemes_treeview.grid(row=2, column=1, padx=5, pady=5)

lexemes_treeview.column("#0", width=0, stretch=False)
lexemes_treeview.column(1, anchor="w", width=220)
lexemes_treeview.column(2, anchor="w", width=220)

lexemes_treeview.heading("#0", text="", anchor="w")
lexemes_treeview.heading(1, text=" Lexeme", anchor="w")
lexemes_treeview.heading(2, text=" Classification", anchor="w")

symbol_header = tk.Label(root, text="Symbol Table", font=("Helvetica", 12), relief="ridge")
symbol_header.grid(row=1, column=2, padx=5, pady=5, sticky='NSEW')

symbol_treeview = ttk.Treeview(root, selectmode="browse", columns=(1, 2), height=20)
symbol_treeview.grid(row=2, column=2, padx=5, pady=5)

symbol_treeview.column("#0", width=0, stretch=False)
symbol_treeview.column(1, anchor="w", width=220)
symbol_treeview.column(2, anchor="w", width=220)

symbol_treeview.heading("#0", text="", anchor="w")
symbol_treeview.heading(1, text=" Identifier", anchor="w")
symbol_treeview.heading(2, text=" Value", anchor="w")


execute_button = ttk.Button(root, text="Execute", style="Accent.TButton", command=execute)
execute_button.grid(row=3, column=0, padx=5, pady=5, sticky="nsew", columnspan=3)

console = scrolledtext.ScrolledText(root, height=20, font=("Helvetica", 12), fg='white', bg="#404040")
console.grid(row=4, column=0, padx=5, pady=5, sticky="nsew", columnspan=3)

root.mainloop()
