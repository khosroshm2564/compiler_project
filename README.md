# Lexical Analyzer

A hand-written, character-by-character lexical analyzer for the first Compiler course assignment. It reads source text from a file or standard input and prints recognized tokens, lexical errors, and token counts. It does not use Lex, Flex, or regular expressions. This project implements only the lexical-analysis assignment; it does not include later compiler stages.

## Supported tokens

| Type | Definition | Examples |
|---|---|---|
| `KEYWORD` | `int`, `float`, `bool`, `if`, `else`, `while`, `return`, `print` | `if`, `int` |
| `IDENTIFIER` | A letter followed by letters or digits | `x`, `value1`, `ifvalue` |
| `INTEGER` | One or more digits | `10`, `1234` |
| `REAL` | One or more digits, a dot, then one or more digits | `3.14`, `12.75` |
| `OPERATOR` | `+`, `-`, `*`, `/`, `=`, `==`, `!=`, `>=`, `<=`, `>`, `<` | `>=`, `==` |
| `SEPARATOR` | `(`, `)`, `{`, `}`, `;`, `,` | `;`, `(` |

Whitespace, tabs, and single-line comments (`// ...`) are skipped and do not produce tokens. The operator set preserves the existing conventional spellings and the PDF's explicit `>=` Maximal Munch example; no additional operator spellings are inferred from the PDF's visually ambiguous right-to-left examples.

## Behavior

- **Maximal Munch:** two-character operators (`==`, `!=`, `>=`, `<=`) are checked before one-character operators.
- **Keywords and identifiers:** the complete word is read before keyword lookup, so `if` is a `KEYWORD` and `ifvalue` is an `IDENTIFIER`.
- **Real numbers:** the dot is part of a real number only when followed by a digit. For example, `12.` produces integer `12` and a lexical error for `.`.
- **Lexical errors:** an invalid character is reported with its line and column, skipped, and scanning continues.
- **Output:** each token is printed on its own line with its type, lexeme, line, and column. Errors and per-type token counts are printed afterward.

## Run

Requires Python 3; there are no external runtime dependencies.

```text
python lexer.py test1.txt
python lexer.py test2.txt
python lexer.py test3.txt
python lexer.py
```

With no file argument, the lexer reads standard input until EOF (Ctrl+Z then Enter in Windows terminals; Ctrl+D in Unix-like terminals).

## Supplied sample runs

These summaries are from running the commands above against the three included input files:

| Input | Output summary |
|---|---|
| `test1.txt` | 19 tokens: 3 `KEYWORD`, 4 `IDENTIFIER`, 4 `OPERATOR`, 3 `INTEGER`, 4 `SEPARATOR`, and 1 `REAL`; reports `@` at line 4, column 12. |
| `test2.txt` | 28 tokens: 14 `IDENTIFIER`, 11 `OPERATOR`, 2 `INTEGER`, and 1 `SEPARATOR`; no lexical errors. |
| `test3.txt` | 16 tokens: 2 `KEYWORD`, 6 `IDENTIFIER`, 3 `OPERATOR`, 3 `INTEGER`, and 2 `SEPARATOR`; reports `_`, `.`, `#`, `@`, `!`, and `.` with their source positions, then continues scanning. |

Each command prints every token and the complete per-type count table, in addition to the error summary.

## Tests

Run the automated unit and command-line tests with Python's standard-library test runner:

```text
python -m unittest -v
```

The tests cover the token classes and rules above, maximal munch, line/column error reporting with continued scanning, token counts, both input modes, and all three supplied sample inputs.

## Project files

| File | Purpose |
|---|---|
| `lexer.py` | The lexical analyzer and command-line interface |
| `test_lexer.py` | Automated tests for assignment requirements and sample inputs |
| `test1.txt` | Declarations, integer/real values, comment, keyword-like identifier, and an invalid character |
| `test2.txt` | Operators, arithmetic, whitespace, and tab |
| `test3.txt` | Invalid characters and malformed real-number examples |
| `test_lexer.py` | Automated unit and command-line tests |
| `outputs/test1_output.txt` | Captured stdout from running the lexer on `test1.txt` |
| `outputs/test2_output.txt` | Captured stdout from running the lexer on `test2.txt` |
| `outputs/test3_output.txt` | Captured stdout from running the lexer on `test3.txt` |
| `Compiler_Project_Report.docx` | Persian assignment report; the personal-analysis section is reserved for students |
| `P_7621303702db4824989e4b509ef10d72.pdf` | Original first-assignment specification |