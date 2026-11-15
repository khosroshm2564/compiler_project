import subprocess
import sys
import unittest
from pathlib import Path

from lexer import Lexer


ROOT = Path(__file__).resolve().parent


class LexerTests(unittest.TestCase):
    def test_keywords_and_identifiers(self):
        source = "int float bool if else while return print ifvalue student2"
        lexer = Lexer(source)

        tokens = lexer.tokenize()

        self.assertEqual(
            [(token.type, token.lexeme) for token in tokens],
            [
                ("KEYWORD", "int"),
                ("KEYWORD", "float"),
                ("KEYWORD", "bool"),
                ("KEYWORD", "if"),
                ("KEYWORD", "else"),
                ("KEYWORD", "while"),
                ("KEYWORD", "return"),
                ("KEYWORD", "print"),
                ("IDENTIFIER", "ifvalue"),
                ("IDENTIFIER", "student2"),
            ],
        )
        self.assertEqual(lexer.errors, [])

    def test_integer_and_real_number_rules(self):
        lexer = Lexer("10 250 1234 3.14 25.5 12.75")

        tokens = lexer.tokenize()

        self.assertEqual(
            [(token.type, token.lexeme) for token in tokens],
            [
                ("INTEGER", "10"),
                ("INTEGER", "250"),
                ("INTEGER", "1234"),
                ("REAL", "3.14"),
                ("REAL", "25.5"),
                ("REAL", "12.75"),
            ],
        )
        self.assertEqual(lexer.errors, [])

    def test_maximal_munch_operators(self):
        source = "== != >= <= + - * / = > <"
        lexer = Lexer(source)

        tokens = lexer.tokenize()

        self.assertEqual(
            [(token.type, token.lexeme) for token in tokens],
            [("OPERATOR", operator) for operator in source.split()],
        )
        self.assertEqual(lexer.errors, [])

    def test_all_separators(self):
        lexer = Lexer("(){};,")

        tokens = lexer.tokenize()

        self.assertEqual(
            [(token.type, token.lexeme) for token in tokens],
            [("SEPARATOR", separator) for separator in "(){};,"],
        )

    def test_whitespace_tabs_and_single_line_comments_are_skipped(self):
        lexer = Lexer("a \t // ignored comment\nb / c")

        tokens = lexer.tokenize()

        self.assertEqual(
            [(token.type, token.lexeme) for token in tokens],
            [
                ("IDENTIFIER", "a"),
                ("IDENTIFIER", "b"),
                ("OPERATOR", "/"),
                ("IDENTIFIER", "c"),
            ],
        )
        self.assertEqual(
            [(token.line, token.column) for token in tokens],
            [(1, 1), (2, 1), (2, 3), (2, 5)],
        )
        self.assertEqual(lexer.errors, [])

    def test_invalid_characters_report_positions_and_scanning_continues(self):
        lexer = Lexer("@x\n# 7")

        tokens = lexer.tokenize()

        self.assertEqual(
            [(token.type, token.lexeme, token.line, token.column) for token in tokens],
            [
                ("IDENTIFIER", "x", 1, 2),
                ("INTEGER", "7", 2, 3),
            ],
        )
        self.assertEqual(
            lexer.errors,
            [("@", 1, 1), ("#", 2, 1)],
        )

    def test_token_counts(self):
        lexer = Lexer("int x = 1;")
        lexer.tokenize()

        self.assertEqual(
            lexer.count_by_type(),
            {
                "KEYWORD": 1,
                "IDENTIFIER": 1,
                "OPERATOR": 1,
                "INTEGER": 1,
                "SEPARATOR": 1,
            },
        )

    def test_three_supplied_sample_inputs(self):
        expected = {
            "test1.txt": (19, [("@", 4, 12)]),
            "test2.txt": (28, []),
            "test3.txt": (
                16,
                [
                    ("_", 1, 7),
                    (".", 1, 16),
                    ("#", 2, 1),
                    ("@", 2, 9),
                    ("!", 3, 1),
                    (".", 4, 11),
                ],
            ),
        }

        for filename, (token_count, errors) in expected.items():
            with self.subTest(filename=filename):
                source = (ROOT / filename).read_text(encoding="utf-8")
                lexer = Lexer(source)
                tokens = lexer.tokenize()

                self.assertEqual(len(tokens), token_count)
                self.assertEqual(lexer.errors, errors)

    def test_command_line_file_input(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "lexer.py"), str(ROOT / "test1.txt")],
            capture_output=True,
            check=True,
            cwd=ROOT,
            text=True,
        )

        self.assertIn("<REAL, '12.5'>", result.stdout)
        self.assertIn("<IDENTIFIER, 'ifvalue'>", result.stdout)
        self.assertIn(
            "Lexical error: invalid character '@' at line 4, column 12",
            result.stdout,
        )
        self.assertIn("TOTAL        19", result.stdout)

    def test_command_line_standard_input(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "lexer.py")],
            capture_output=True,
            check=True,
            cwd=ROOT,
            input="int x=1;",
            text=True,
        )

        self.assertIn("<KEYWORD, 'int'>", result.stdout)
        self.assertIn("<IDENTIFIER, 'x'>", result.stdout)
        self.assertIn("<INTEGER, '1'>", result.stdout)
        self.assertIn("No errors.", result.stdout)
        self.assertIn("TOTAL        5", result.stdout)


if __name__ == "__main__":
    unittest.main()
