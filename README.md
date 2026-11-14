# Lexical Analyzer in Python

A hand-written lexical analyzer (scanner) for a small C-like language, built for the Compiler course exercise. It does not use Lex, Flex, or regular expressions. The scanner works character by character.

## Supported tokens

| Type | Description | Examples |
|---|---|---|
| KEYWORD | `int float bool if else while return print` | `if`, `int` |
| IDENTIFIER | A letter followed by letters or digits | `x`, `value1`, `ifvalue` |
| INTEGER | One or more digits | `10`, `1234` |
| REAL | Digits, a dot, then digits | `3.14`, `12.75` |
| OPERATOR | `+ - * / = == != >= <= > <` | `>=`, `==` |
| SEPARATOR | `( ) { } ; ,` | `;`, `(` |

Whitespace, tabs, and single-line comments (`// ...`) are skipped and produce no tokens.

## How it works

- **Maximal Munch:** at each step the longest valid token is taken. Two-character operators (`==`, `!=`, `>=`, `<=`) are checked before one-character ones.
- **Keywords vs. identifiers:** the whole word is read first, then compared with the keyword set. So `if` is a KEYWORD and `ifvalue` is an IDENTIFIER.
- **Real numbers:** a dot is consumed only if a digit follows it, so `12.` becomes INTEGER `12` plus an invalid `.`.
- **Error handling:** an invalid character (such as `@`, `#`, `_`, or a lone `!`) is reported with its line and column, skipped, and scanning continues.

## Usage

Requires Python 3.

```
python3 lexer.py test1.txt     # read from a file
python3 lexer.py               # read from standard input (end with Ctrl+D)
```

## Output

1. Every token on its own line: `<TYPE, 'lexeme'>` with its line and column.
2. All lexical errors with line and column.
3. A count of tokens per type and a total.

## Files

| File | Purpose |
|---|---|
| `lexer.py` | The lexical analyzer |
| `test1.txt` | Variable declarations, numbers, comment, `if` vs `ifvalue`, one error |
| `test2.txt` | One- and two-character operators, extra spaces and tabs |
| `test3.txt` | Several lexical errors in a row (`_`, `.`, `#`, `@`, `!`) |

## Sample

Input:

```
int number = 25;
ifvalue != @ 3
```

Output (shortened):

```
<KEYWORD, 'int'>
<IDENTIFIER, 'number'>
<OPERATOR, '='>
<INTEGER, '25'>
<SEPARATOR, ';'>
<IDENTIFIER, 'ifvalue'>
<OPERATOR, '!='>
<INTEGER, '3'>
Lexical error: invalid character '@' at line 2, column 12
```