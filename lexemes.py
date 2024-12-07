import re
import tkinter as tk
from tkinter import filedialog

class Lexemes:
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value

keywords = {
    r'^HAI$': 'Code Delimiter',
    r'^KTHXBYE$': 'Code Delimiter',
    r'^WAZZUP$': 'Variable Declaration Delimiter',
    r'^BUHBYE$': 'Variable Declaration Delimiter',
    r'^BTW .*': 'Comment',
    r'^OBTW .*': 'Comment',
    r'^TLDR$': 'Comment Delimiter',
    r'^I HAS A [a-zA-Z][a-zA-Z0-9_]*$': 'Variable Declaration',
    r'^I HAS A [a-zA-Z][a-zA-Z0-9_]* ITZ .+$': 'Variable Declaration and Initialization',
    r'^ITZ$': 'Variable Assignment',
    r'^R .+$': 'Variable Assignment',
    r'^SUM OF .+$': 'Arithmetic Operation',
    r'^DIFF OF .+$': 'Arithmetic Operation',
    r'^PRODUKT OF .+$': 'Arithmetic Operation',
    r'^QUOSHUNT OF .+$': 'Arithmetic Operation',
    r'^MOD OF .+$': 'Arithmetic Operation',
    r'^BIGGR OF .+$': 'Arithmetic Operation',
    r'^SMALLR OF .+$': 'Arithmetic Operation',
    r'^BOTH OF .+$': 'Boolean Operation',
    r'^EITHER OF .+$': 'Boolean Operation',
    r'^WON OF .+$': 'Boolean Operation',
    r'^NOT .+$': 'Boolean Operation',
    r'^ANY OF .+$': 'Boolean Operation',
    r'^ALL OF .+$': 'Boolean Operation',
    r'^BOTH SAEM .+$': 'Comparison Operation',
    r'^DIFFRINT .+$': 'Comparison Operation',
    r'^SMOOSH .+$': 'String Concatenation',
    r'^MAEK .+$': 'Typecasting Operation',
    r"^A$": "A",
    r'^IS NOW A .+$': 'Typecasting Operation',
    r'^VISIBLE .+$': 'Output Keyword',
    r'^GIMMEH .+$': 'Input Keyword',
    r'^O RLY\?$': 'If-then Keyword',
    r'^YA RLY$': 'If-then Keyword',
    r'^MEBBE .+$': 'If-then Keyword',
    r'^NO WAI$': 'If-then Keyword',
    r'^OIC$': 'If-then Keyword',
    r'^WTF\?$': 'Switch-Case Keyword',
    r'^OMG .+$': 'Switch-Case Keyword',
    r'^IM IN YR .+$': 'Loop Keyword',
    r'^UPPIN .+$': 'Loop Operation',
    r'^NERFIN .+$': 'Loop Operation',
    r'^YR .+$': 'Parameter Delimiter',
    r'^TIL .+$': 'Loop Keyword',
    r'^WILE .+$': 'Loop Keyword',
    r'^IM OUTTA YR .+$': 'Loop Keyword',
    r'^HOW IZ I .+$': 'Function Keyword',
    r'^IF U SAY SO$': 'Function Keyword',
    r'^GTFO$': 'Return Keyword',
    r'^FOUND YR .+$': 'Return Keyword',
    r'^I IZ .+$': 'Function Call',
    r'^MKAY$': 'Concatenation Delimiter',
    r'^NOOB$': 'Void Literal',
    r'^AN$': 'Parameter Delimiter'
}

class Lexer:
    def __init__(self, source_code):
        self.source_code = source_code.splitlines()
        self.tokens = []

    def tokenize(self):
        for line in self.source_code:
            line = line.strip()
            if line:
                matched = False
                for pattern, token_type in keywords.items():
                    if re.match(pattern, line):
                        self.tokens.append(Lexemes(token_type, line))
                        matched = True
                        break
                if not matched:
                    print("Lexeme unidentified")
                    break
        return self.tokens

def output_print(file_path):
    with open(file_path, 'r') as file:
        source_code = file.read()
    lexer = Lexer(source_code)
    tokens = lexer.tokenize()
    for token in tokens:
        print(f"{token.value}: {token.keyword}")

def open_file():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        output_print(file_path)

if __name__ == "__main__":
    open_file()
