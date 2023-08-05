import unittest

from simple_ast import BinOp, Token, Num, INTEGER, MUL, PLUS


class TestBinOp(unittest.TestCase):
    def test_simple(self):
        mul_node = BinOp(
            left=Num(Token(INTEGER, 2)),
            op=Token(MUL, '*'),
            right=Num(Token(INTEGER, 7))
        )
        add_node = BinOp(
            left=mul_node,
            op=Token(PLUS, '+'),
            right=Num(Token(INTEGER, 3))
        )
