import re
import tkinter as tk
from tkinter import filedialog

class Interpreter:
    def __init__(self, root):
        self.root = root
        self.root.title("LOLCode Interpreter")
        self.file_path = filedialog.askopenfilename(title="Select a file")
        self.variables = {}
        self.functions = {}
        self.loops = {}
        self.comment_block = False
        self.lines = []
        self.gui_widgets()

    def gui_widgets(self):
        self.canvas = tk.Canvas(self.root, width=300, height=300, bg='white', borderwidth=0, highlightthickness=0, relief=tk.SOLID)
        self.canvas.pack(side=tk.TOP, padx=(2, 0), pady=(2, 0))
        self.mainloop()

    def tokenize(self, line):
        token_pattern = r'"[^"]*"|\S+|[.]'  
        complex_tokens = ['SUM OF', 'PRODUKT OF', 'BIGGR OF', 'DIFF OF', 'QUOSHUNT OF']

        for complex_token in complex_tokens:
            line = line.replace(complex_token, complex_token.replace(" ", "_"))

        tokens = re.findall(token_pattern, line.strip())
        tokens = [token.replace("_", " ") for token in tokens]

        return tokens

    def parser(self, tokens):
        if not tokens:
            return None

        keywords = {
            "HAI": r"^HAI$",
            "KTHXBYE": r"^KTHXBYE$",
            "WAZZUP": r"^WAZZUP$",
            "BUHBYE": r"^BUHBYE$",
            "BTW": r"^BTW.$",
            "OBTW": r"^OBTW$",
            "TLDR": r"^TLDR$",
            "I HAS A": r"^I HAS A (\w+)(?: ITZ (.+))?$",
            "VISIBLE": r"^VISIBLE (\w+)(?: (.+))?$",
            "GIMMEH": r"^GIMMEH (.+)$",
            "O RLY?": r"^O RLY\?$",
            "YA RLY": r"^YA RLY$",
            "MEBBE": r"^MEBBE$",
            "NO WAI": r"^NO WAI$",
            "OIC": r"^OIC$",
            "WTF?": r"^WTF\?$",
            "OMG": r"^OMG$",
            "IM IN YR": r"^IM IN YR$",
            "UPPIN": r"^UPPIN$",
            "NERFIN": r"^NERFIN$",
            "YR": r"^YR$",
            "TIL": r"^TIL$",
            "WILE": r"^WILE$",
            "IM OUTTA YR": r"^IM OUTTA YR$",
            "HOW IZ I": r"^HOW IZ I$",
            "IF U SAY SO": r"^IF U SAY SO$",
            "GTFO": r"^GTFO$",
            "FOUND YR": r"^FOUND YR$",
            "I IZ": r"^I IZ$",
            "MKAY": r"^MKAY$",
            "AN": r"^AN$",
            "BOTH SAEM": r"^BOTH SAEM (\w+)(?: AN (.+))?$"
        }

        # Updated regex for valid identifiers: Must start with a letter and cannot start with a digit
        identifier_pattern = r'^[A-Za-z][A-Za-z0-9_]*$'  # Valid identifier pattern

        # Ignore comments if there is a 'BTW' or 'OBTW'
        if "BTW" in tokens:
            tokens = tokens[:tokens.index("BTW")]

        for keyword, pattern in keywords.items():
            match = re.match(pattern, ' '.join(tokens))
            if match:
                if keyword == "I HAS A":
                    variable = match.group(1)
                    variable_value = match.group(2)

                    # Apply identifier regex check here
                    if not re.match(identifier_pattern, variable):
                        return f"Error: Invalid variable identifier '{variable}'"

                    # Check if variable_value is valid
                    if variable_value and not self.is_valid_literal_or_expression(variable_value):
                        return f"Error: Invalid literal or expression for variable '{variable}'"

                    if variable_value:
                        self.variables[variable] = variable_value
                        return f"Variable '{variable}' is assigned: {self.variables[variable]}"
                    else:
                        self.variables[variable] = "NOOB"
                        return f"Variable '{variable}' is assigned default value: {self.variables[variable]}"

                if keyword == "VISIBLE":
                    variable = match.group(1)
                    variable_value = match.group(2)

                    # Apply identifier regex check here
                    if not re.match(identifier_pattern, variable):
                        return f"Error: Invalid variable identifier '{variable}'"

                    # Check if variable_value is valid
                    if variable_value and not self.is_valid_literal_or_expression(variable_value):
                        return f"Error: Invalid literal or expression for variable '{variable}'"

                    if variable_value:
                        self.variables[variable] = variable_value
                        return f"Output: '{variable}'"
                    else:
                        self.variables[variable] = "NOOB"
                        return f"Output '{variable}'"
                
                    return f"Output: {value}"

                if keyword == "BTW":
                    return f"Comment: {' '.join(tokens[1:])}"
                
                if keyword == "HAI":
                    return f"Start of program: {keyword}"
                
                if keyword == "KTHXBYE":
                    return f"End of program: {keyword}"

                if keyword == "WILE" or keyword == "TIL":
                    loop_id = match.group(0)  # Extract the loop identifier
                    # Apply the identifier regex here too
                    if not re.match(identifier_pattern, loop_id):
                        return f"Error: Invalid loop identifier '{loop_id}'"
                    return f"Loop starts with identifier '{loop_id}'"

                if keyword == "BOTH SAEM":
                    compare1 = match.group(1)
                    compare2 = match.group(2)

                    if not re.match(identifier_pattern, compare1) and not self.is_valid_literal(compare1):
                        return f"Error: Invalid variable or literal '{compare1}'."
                    if not re.match(identifier_pattern, compare2) and not self.is_valid_literal(compare2):
                        return f"Error: Invalid variable or literal '{compare2}'."
            
                    return f"Comparison: '{compare1}' == '{compare2}'"

                return f"Lexeme: {keyword}"


    def is_valid_literal_or_expression(self, value):
        numbr = r'^-?[0-9]+$'  # Integer literal
        numbar = r'^-?[0-9]+\.[0-9]+$'  # Floating-point literal
        yarn = r'^".*"$'  # String literal
        troof = r'^(WIN|FAIL)$'  # Boolean literal

        # Check if value is a valid literal or a valid expression (like SUM OF, etc.)
        complex_patterns = r'^(SUM OF .*|DIFF OF .*|PRODUKT OF .*|QUOSHUNT OF .*)$'

        return re.match(numbr, value) or re.match(numbar, value) or re.match(yarn, value) or re.match(troof, value) or re.match(complex_patterns, value)

    def is_valid_literal(self, value):
        # Basic check for valid literals (without expressions)
        numbr = r'^-?[0-9]+$'
        numbar = r'^-?[0-9]+\.[0-9]+$'
        yarn = r'^".*"$'
        troof = r'^(WIN|FAIL)$'

        return re.match(numbr, value) or re.match(numbar, value) or re.match(yarn, value) or re.match(troof, value)

    def extract(self, line):
        if line == "OBTW":
            self.comment_block = True
            return

        if self.comment_block:
            if line == "TLDR":
                self.comment_block = False
            return

        tokens = self.tokenize(line)
        parsed = self.parser(tokens)

        if parsed:
            print(parsed)
            return parsed  

    def mainloop(self):
        # Read and process the LOLCode file
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    self.lines.append(line)

            first_non_comment_line = None
            for line in self.lines:
                if line and not line.startswith(('OBTW', 'BTW', 'TLDR')):
                    first_non_comment_line = line
                    break

            if not first_non_comment_line or first_non_comment_line != "HAI":
                print("Error: Program must start with 'HAI'")
                return  

            with open(self.file_path, 'r') as file:
                for line in file:
                    line = line.strip()
                    self.extract(line)

            # Check for the program's end with 'KTHXBYE'
            if not self.lines[-1].strip() == "KTHXBYE":
                print("Error: Program must end with 'KTHXBYE'.")
                return  

        except FileNotFoundError:
            print("Error: File not found!")

root = tk.Tk()
app = Interpreter(root)
root.mainloop()
