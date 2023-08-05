import unittest

from simple_ast import Lexer, Token, INTEGER, EOF, SYNTAX_ERROR_WRONG_OPERATION


class TestLexer(unittest.TestCase):
    def test_simple_arithmetic(self):
        lexer = Lexer("1 + 1")
        self.assertEqual(lexer.get_next_token(), Token(INTEGER, 1))

    def test_syntax_error(self):
        with self.assertRaises(SyntaxError) as error:
            lexer = Lexer("1 % ")
            while lexer.get_next_token() != Token(EOF, None):
                continue
        self.assertEqual(error.exception.args,
                         (SYNTAX_ERROR_WRONG_OPERATION % '%',))
