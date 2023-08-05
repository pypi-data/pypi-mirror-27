import unittest

from simple_ast import Lexer, Parser, Interpreter


class TestInterpreter(unittest.TestCase):
    def test_simple(self):
        raw_expression = "1 + 1 - 2 * 3"
        result = Interpreter(Parser(Lexer(raw_expression))).interpret()
        self.assertEqual(result, -4)

        raw_expression = "1 + 1 + 1 + 2"
        result = Interpreter(Parser(Lexer(raw_expression))).interpret()
        self.assertEqual(result, 5)

    def test_compound(self):
        raw_expression = "(1 + 1) / (100 - 98)"
        result = Interpreter(Parser(Lexer(raw_expression))).interpret()
        self.assertEqual(result, 1)
