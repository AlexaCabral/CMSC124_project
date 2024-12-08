import re

class Interpreter:
    def __init__(self, console):
        self.console = console
        self.variables = {}
        self.comment_block = False
        self.lexemes = []  

    def add_to_console(self, message):
        self.console.insert("end", message + "\n")
        self.console.yview("end")

    def tokenize(self, line):
        token_pattern = r'"[^"]*"|\S+|[.]'  
        tokens = re.findall(token_pattern, line.strip())

        # Replace complex tokens like "SUM OF" and similar with underscores to simplify tokenization
        complex_tokens = ['SUM OF', 'PRODUKT OF', 'BIGGR OF', 'DIFF OF', 'QUOSHUNT OF']
        
        for complex_token in complex_tokens:
            line = line.replace(complex_token, complex_token.replace(" ", "_"))
        
        tokens = re.findall(token_pattern, line.strip())

        tokens = [token.replace("_", " ") for token in tokens]
        
        return tokens

    def evaluate_expression(self, expr):
        """Evaluate a simple arithmetic expression, substituting variables."""
        try:
            # Replace variable names with their values
            for var, value in self.variables.items():
                expr = expr.replace(var, str(value))

            # Handle operations (SUM OF, PRODUKT OF, DIFF OF, QUOSHUNT OF, BIGGR OF)
            expr = self.evaluate_operations(expr)

            # Evaluate the expression (now with substituted variables and operators)
            result = eval(expr)
            return result
        except ZeroDivisionError:
            return "Error: Division by zero."
        except Exception as e:
            return f"Error: Invalid expression - {str(e)}"

    def evaluate_operations(self, expr):
        """Evaluate LOLCODE specific operations."""
        # Handle "SUM OF" -> "+"
        expr = re.sub(r"SUM OF (\S+) AN (\S+)", r"(\1 + \2)", expr)

        # Handle "PRODUKT OF" -> "*"
        expr = re.sub(r"PRODUKT OF (\S+) AN (\S+)", r"(\1 * \2)", expr)

        # Handle "DIFF OF" -> "-"
        expr = re.sub(r"DIFF OF (\S+) AN (\S+)", r"(\1 - \2)", expr)

        # Handle "QUOSHUNT OF" -> "/"
        expr = re.sub(r"QUOSHUNT OF (\S+) AN (\S+)", r"(\1 / \2)", expr)

        # Handle "BIGGR OF" -> "max()"
        expr = re.sub(r"BIGGR OF (\S+) AN (\S+)", r"max(\1, \2)", expr)

        return expr

    def parser(self, tokens):
        if not tokens:
            return None

        keywords = {
            "HAI": r"^HAI$",
            "KTHXBYE": r"^KTHXBYE$",
            "WAZZUP": r"^WAZZUP$",
            "BUHBYE": r"^BUHBYE$",
            "BTW": r"^BTW (.*)$",
            "OBTW": r"^OBTW$",
            "TLDR": r"^TLDR$",
            "I HAS A": r"^I HAS A (\w+)(?: ITZ (.+))?$",
            "VISIBLE": r"^VISIBLE ((.|\w)+)(?: (.+))?$",
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

        for keyword, pattern in keywords.items():
            match = re.match(pattern, ' '.join(tokens))
            if match:
                if keyword == "I HAS A":
                    variable = match.group(1)
                    variable_value = match.group(2) if match.group(2) else "NOOB"
                    self.variables[variable] = variable_value
                    self.lexemes.append((keyword, "Variable Declaration"))
                    self.lexemes.append(("ITZ", "Variable Initialization"))
                    self.lexemes.append((variable, "Variable Identifier"))
                    return

                if keyword == "VISIBLE":
                    variable = match.group(1).strip()
                    variable_pattern = r'^[A-Za-z]+[0-9A-Za-z_]*$'

                    self.evaluate_expression(variable)

                    if variable.startswith('"') and variable.endswith('"'):
                        self.add_to_console(variable[1:-1])
                        self.lexemes.append((variable, "Literal"))
                    elif variable in self.variables:
                        self.add_to_console(str(self.variables[variable]))
                    elif variable.split()[0] in self.variables :
                            self.add_to_console(self.variables[variable.split()[0]])
                    
                    if not re.match(variable_pattern, variable):
                        return f"Error: Invalid variable '{variable}'."
                        break
                    self.lexemes.append((keyword, "Output Keyword"))
                    self.lexemes.append((variable, "Variable Identifier"))
                    return

                if keyword == "BTW":
                    value = ' '.join(tokens[1:])
                    self.lexemes.append((keyword, "Comment Keyword"))
                    self.lexemes.append((value, "Comment Line"))
                    return

                if keyword == "GIMMEH":
                    variable = match.group(1).strip()
                    variable_pattern = r'^[A-Za-z]+[0-9A-Za-z_]*$'

                    if not re.match(variable_pattern, variable):
                        return f"Error: Invalid variable '{variable}'."

                    self.lexemes.append((keyword, "Input Keyword"))
                    self.lexemes.append((variable, "Variable Identifier"))

                if keyword == "HAI":
                    self.lexemes.append((keyword, "Start of Program"))

                if keyword == "KTHXBYE":
                    self.lexemes.append((keyword, "End of Program"))

                if keyword == "BUHBYE":
                    self.lexemes.append((keyword, "End of Variable Declaration"))

                if keyword == "WAZZUP":
                    self.lexemes.append((keyword, "Start of Variable Declaration"))

                if keyword == "O RLY?":
                    self.lexemes.append((keyword, "Start of Conditional Identifier"))

                if keyword == "YA RLY?":
                    self.lexemes.append((keyword, "Conditional If Identifier"))

                if keyword == "NO WAI":
                    self.lexemes.append((keyword, "Conditional Else Identifier"))

                if keyword == "MEBBE":
                    value = {' '.join(tokens[1:])}
                    self.lexemes.append((keyword, "Conditional Else-If Identifier"))

                if keyword == "OIC":
                    self.lexemes.append((keyword, "End of Conditional Declaration"))

                if keyword == "BOTH SAEM":
                    compare1 = match.group(1)
                    compare2 = match.group(2)

                    variable_pattern = r'^([A-Za-z]+[0-9A-Za-z_]*)|[0-9]+$'

                    if not re.match(variable_pattern, compare1):
                        return f"Error: Invalid variable or literal '{compare1}'."
                    if not re.match(variable_pattern, compare2):
                        return f"Error: Invalid variable or literal '{compare2}'."

                    value = {compare1} == {compare2}
                    self.lexemes.append((keyword, "Comparison Identifier"))

        return None

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

    def process_code(self, code_lines):
        for line in code_lines:
            line = line.strip()
            if line:
                self.extract(line)

    def get_lexemes(self):
        return self.lexemes  

    def get_variables(self):
        return self.variables
