import re
import tkinter as tk
from tkinter import filedialog
lexemes_list = []
class Lexemes:
    def __init__(self, keyword, value):
        self.keyword = keyword
        self.value = value
        

keywords = {
    r'^HAI$': 'Code Delimiter',
    r'^KTHXBYE$': 'Code Delimiter',
    r'^WAZZUP$': 'Variable Declaration Delimiter',
    r'^BUHBYE$': 'Variable Declaration Delimiter',
    r'^BTW$': 'Comment Delimiter',
    r'^OBTW$': 'Comment Delimiter',
    r'^TLDR$': 'Comment Delimiter',
    r'^I HAS A$': 'Variable Declaration',
    r'^ITZ$': 'Variable Assignment',
    r'^R$': 'Variable Assignment',
    r'^SUM OF$': 'Arithmetic Operation',
    r'^DIFF OF$': 'Arithmetic Operation',
    r'^PRODUKT OF$': 'Arithmetic Operation',
    r'^QUOSHUNT OF$': 'Arithmetic Operation',
    r'^MOD OF$': 'Arithmetic Operation',
    r'^BIGGR OF$': 'Arithmetic Operation',
    r'^SMALLR OF$': 'Arithmetic Operation',
    r'^BOTH OF$': 'Boolean Operation',
    r'^EITHER OF$': 'Boolean Operation',
    r'^WON OF$': 'Boolean Operation',
    r'^NOT$': 'Boolean Operation',
    r'^ANY OF$': 'Boolean Operation',
    r'^ALL OF$': 'Boolean Operation',
    r'^BOTH SAEM$': 'Comparison Operation',
    r'^DIFFRINT$': 'Comparison Operation',
    r'^SMOOSH$': 'String Concatenation',
    r'^MAEK$': 'Typecasting Operation',
    r"^A$": "A",
    r'^IS NOW A$': 'Typecasting Operation',
    r'^VISIBLE$': 'Output Keyword',
    r'^GIMMEH$': 'Input Keyword',
    r'^O RLY\?$': 'If-then Keyword',
    r'^YA RLY$': 'If-then Keyword',
    r'^MEBBE$': 'If-then Keyword',
    r'^NO WAI$': 'If-then Keyword',
    r'^OIC$': 'If-then Keyword',
    r'^WTF\?$': 'Switch-Case Keyword',
    r'^OMG$': 'Switch-Case Keyword',
    r'^IM IN YR$': 'Loop Keyword',
    r'^UPPIN$': 'Loop Operation',
    r'^NERFIN$': 'Loop Operation',
    r'^YR$': 'Parameter Delimiter',
    r'^TIL$': 'Loop Keyword',
    r'^WILE$': 'Loop Keyword',
    r'^IM OUTTA YR$': 'Loop Keyword',
    r'^HOW IZ I$': 'Function Keyword',
    r'^IF U SAY SO$': 'Function Keyword',
    r'^GTFO$': 'Return Keyword',
    r'^FOUND YR$': 'Return Keyword',
    r'^I IZ$': 'Function Call',
    r'^MKAY$': 'Concatenation Delimiter',
    r'^NOOB$': 'Void Literal',
    r'^AN$': 'Parameter Delimiter',
    
    r'^".*"$': 'YARN Literal',
    r'^(NUMBR|NUMBAR|YARN|TROOF|NOOB)$': 'Data Type Literal',
    r'^(WIN|FAIL)$': 'TROOF Literal',
    r'^[a-zA-Z][a-zA-Z0-9_]*$': 'Variable Identifier',
    r'^-?(0|[1-9][0-9]*)?\.[0-9]+$': 'NUMBAR Literal',
    r'^-?0|-?[1-9][0-9]*$': 'NUMBR Literal',
}

compiled_keywords = [(re.compile(pattern), label) for pattern, label in keywords.items()]

def classify_token(token):
    for pattern, label in compiled_keywords:
        if pattern.match(token):
            return label
    return "Literal"

def evaluate(lines):
    result = []
    multiline_comment = False
    multiline_comment_content = []

    for line in lines:
        stripped_line = line.strip()
        if multiline_comment:
            if re.match(r"^TLDR$", stripped_line):
                result.append(["OBTW", "Comment Delimiter"])
                result.append([" ".join(multiline_comment_content), "Comment"])
                result.append(["TLDR", "Comment Delimiter"])
                multiline_comment = False
                multiline_comment_content = []
            else:
                multiline_comment_content.append(stripped_line)
            continue

        if re.match(r"^OBTW$", stripped_line):
            multiline_comment = True
            continue

        while stripped_line:
            # Match multi-word and single-word keywords
            match = re.search(r"\b(" + "|".join(keywords.keys()).replace("^", "").replace("$", "") + r")\b", stripped_line)
            if match:
                # Capture everything before the match as separate tokens (if exists)
                prefix = stripped_line[:match.start()].strip()
                if prefix:
                    prefix_tokens = re.findall(r'\S+', prefix)
                    for token in prefix_tokens:
                        result.append([token, classify_token(token)])
                # Add the matched keyword
                token = match.group(0)
                token_class = classify_token(token)
                
                if token == "I HAS A":
                    # Handle variable declaration with declaration
                    rest = stripped_line[match.end():].strip()
                    var_match = re.match(r'^([a-zA-Z][a-zA-Z0-9_]*)', rest) # variable
                    
                    if var_match and (literal := rest[len(var_match.group(0)):].strip()).startswith("ITZ"):
                        variable = var_match.group(0)
                        result.append([token, token_class])
                        result.append([variable, "Variable Identifier"])
                        result.append(["ITZ", "Variable Assignment"])
                        
                        # Handle the literal if YARN literal or another data type
                        literal_value = literal[3:].strip()
                        if literal_value.startswith('"') and literal_value.endswith('"'):
                            result.append([literal_value.strip('"'), "YARN Literal"])
                        else:
                            result.append([literal_value, classify_token(literal_value)])
                        
                        stripped_line = ""
                        break
                    elif var_match:
                        result.append([token, token_class])
                        result.append([var_match.group(0), "Variable Identifier"])
                        break
                        

                elif token == "VISIBLE" and re.match(r'^".*"$', stripped_line[match.end():].strip()):
                    # Capture the rest of the line as the YARN literal if it matches
                    result.append([token, token_class])
                    result.append([stripped_line[match.end():].strip().strip('"'), "YARN Literal"])
                    break
                elif token == "BTW":
                    comment = stripped_line[match.end():].strip()
                    if comment:
                        result.append([token, token_class])
                        result.append([comment, "Comment"])
                    else:
                        result.append([token, token_class])
                    break
                else:
                    result.append([token, token_class])
                # Remove the matched
                stripped_line = stripped_line[match.end():].strip()
            else:
                # If no keywords match, split the rest of the line into tokens
                for token in re.findall(r'\S+', stripped_line):
                    result.append([token, classify_token(token)])
                break

    # Save lexemes
    lexemes_list.extend([Lexemes(keyword=token[0], value=token[1]) for token in result])
    return result