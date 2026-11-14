"""
Lexical Analyzer (manual implementation, no Lex/Flex/regex)

Usage:
    python lexer.py input.txt      # read source from a file
    python lexer.py                # read source from standard input
"""

import sys

# ---------------------------------------------------------------
# Token definitions
# ---------------------------------------------------------------
KEYWORDS = {"int", "float", "bool", "if", "else", "while", "return", "print"}

OPERATORS_2 = {"==", "!=", ">=", "<="}                 # two-character operators
OPERATORS_1 = {"+", "-", "*", "/", "=", ">", "<"}      # one-character operators
SEPARATORS = {"(", ")", "{", "}", ";", ","}


def is_letter(c):
    return ("a" <= c <= "z") or ("A" <= c <= "Z")


def is_digit(c):
    return "0" <= c <= "9"


def is_letter_or_digit(c):
    return is_letter(c) or is_digit(c)


class Token:
    def __init__(self, type_, lexeme, line, column):
        self.type = type_
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __str__(self):
        return f"<{self.type}, '{self.lexeme}'>  (line {self.line}, col {self.column})"


# ---------------------------------------------------------------
# Lexer
# ---------------------------------------------------------------
class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0          # index of the current character
        self.line = 1
        self.column = 1
        self.tokens = []
        self.errors = []      # list of (char, line, column)

    def peek(self, offset=0):
        """Look at a character without consuming it ('' at end of input)."""
        i = self.pos + offset
        if i < len(self.source):
            return self.source[i]
        return ""

    def advance(self):
        """Consume one character and update line/column."""
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def skip_whitespace_and_comments(self):
        while self.peek() != "":
            ch = self.peek()
            if ch in " \t\r\n":
                self.advance()
            elif ch == "/" and self.peek(1) == "/":
                # single-line comment: skip until end of line
                while self.peek() != "" and self.peek() != "\n":
                    self.advance()
            else:
                break

    def make_token(self, type_, lexeme, line, column):
        tok = Token(type_, lexeme, line, column)
        self.tokens.append(tok)
        return tok

    def next_token(self):
        """Scan one token. Returns False when input is finished."""
        self.skip_whitespace_and_comments()

        ch = self.peek()
        if ch == "":
            return False

        start_line, start_col = self.line, self.column

        # 1) Identifier or Keyword
        if is_letter(ch):
            lexeme = ""
            while is_letter_or_digit(self.peek()):
                lexeme += self.advance()
            type_ = "KEYWORD" if lexeme in KEYWORDS else "IDENTIFIER"
            self.make_token(type_, lexeme, start_line, start_col)
            return True

        # 2) Integer or Real
        if is_digit(ch):
            lexeme = ""
            while is_digit(self.peek()):
                lexeme += self.advance()
            # Real: a dot followed by at least one digit
            if self.peek() == "." and is_digit(self.peek(1)):
                lexeme += self.advance()  # the dot
                while is_digit(self.peek()):
                    lexeme += self.advance()
                self.make_token("REAL", lexeme, start_line, start_col)
            else:
                self.make_token("INTEGER", lexeme, start_line, start_col)
            return True

        # 3) Two-character operator (Maximal Munch: check before one-char)
        two = ch + self.peek(1)
        if two in OPERATORS_2:
            self.advance()
            self.advance()
            self.make_token("OPERATOR", two, start_line, start_col)
            return True

        # 4) One-character operator
        if ch in OPERATORS_1:
            self.advance()
            self.make_token("OPERATOR", ch, start_line, start_col)
            return True

        # 5) Separator
        if ch in SEPARATORS:
            self.advance()
            self.make_token("SEPARATOR", ch, start_line, start_col)
            return True

        # 6) Invalid character: report error, skip it, keep scanning
        bad = self.advance()
        self.errors.append((bad, start_line, start_col))
        return True

    def tokenize(self):
        while self.next_token():
            pass
        return self.tokens

    def count_by_type(self):
        counts = {}
        for tok in self.tokens:
            counts[tok.type] = counts.get(tok.type, 0) + 1
        return counts


# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------
def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], encoding="utf-8") as f:
            source = f.read()
    else:
        print("Enter source code (end with Ctrl+D / Ctrl+Z then Enter):")
        source = sys.stdin.read()

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    print("\n--- Tokens ---")
    for tok in tokens:
        print(tok)

    print("\n--- Lexical Errors ---")
    if lexer.errors:
        for bad, line, col in lexer.errors:
            print(f"Lexical error: invalid character '{bad}' at line {line}, column {col}")
    else:
        print("No errors.")

    print("\n--- Token Count ---")
    for type_, n in lexer.count_by_type().items():
        print(f"{type_:<12} {n}")
    print(f"{'TOTAL':<12} {len(tokens)}")


if __name__ == "__main__":
    main()