import operator

INTEGER, EOF = 'INTEGER', 'EOF'
PLUS, MINUS = 'PLUS', 'MINUS'
DIV, MUL = 'DIV', 'MUL'
LPAREN, RPAREN = 'LPAREN', 'RPAREN'

OP_MAP = {
    PLUS: operator.add,
    MINUS: operator.sub,
    DIV: operator.floordiv,
    MUL: operator.mul
}
OP_TYPE_MAP = {
    "+": PLUS,
    "-": MINUS,
    "/": DIV,
    "*": MUL
}
SYNTAX_ERROR_WRONG_OPERATION = "Wrong operation: `%s`"


class AST(object):
    pass


class BinOp(AST):
    """
    Binary Operation Node, +, -, /, *, etc

    :param Token left: left hand operand
    :param Token op: binary operation token
    :param Token right: right hand operand
    """
    __slots__ = ['left', 'op', 'right']

    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    __slots__ = ['token', 'value']

    def __init__(self, token):
        self.token = token
        self.value = token.value


class Token(object):
    __slots__ = ['type', 'value']

    def __init__(self, type, value):
        #: token type: INTEGER, PLUS, MINUS, EOF
        self.type = type
        #: token value: integers, "+", "-", None
        self.value = value

    def __str__(self):
        """
        Examples::

            Token(INTEGER, 3)
            Token(PLUS, "+")
            Token(MUL, "*")
            Token(LPAREN, "(")
        :rtype: str
        :return: self string object
        """

        return '{class_name}({type}, {value})'.format(
            class_name=self.__class__.__name__,
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return other.type == self.type and self.value == other.value


class Lexer(object):
    def __init__(self, text):
        #: client string input, e.g. "3 + 5", "12 - 5", etc
        self.text = text

        #: position of the parsing text
        self.pos = 0

        #: current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]

    # Lexer code

    def error(self, msg=None):
        raise SyntaxError(msg or "Error parsing input")

    def advance(self):
        """
        Advance the ``pos`` pointer and set the ``current_char`` variable.

        :rtype: None
        :return: None
        """
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # End of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multidigit) integer consumed from input"""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            op_type = OP_TYPE_MAP.get(self.current_char)
            if op_type is None:
                self.error(SYNTAX_ERROR_WRONG_OPERATION % self.current_char)

            self.advance()
            return Token(op_type, self.current_char)

        return Token(EOF, None)


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise SyntaxError("Invalid syntax")

    def eat(self, token_type):
        """
        compares the current token type with the passed token type and if they
        match then `eat` the current token and assign the next token to the
        self.current_token otherwise raise an exception.

        :param str token_type: a token type
        :rtype: None
        :return: None
        """
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor ::= INTEGER"""

        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)

        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def term(self):
        """ term ::= factor ((MUL | DIV) factor)*"""

        node = self.factor()
        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.factor())
        return node

    def expr(self):
        """
        Arithmetic expression parser / interpreter.

        expr ::= term ((PLUS | MINUS) term)*
        term  ::= factor ((MUL | DIV) factor)*
        factor ::= INTEGER

        Example::
            7 + 3 * (10 / (12 / (3 + 1) - 1))

        :rtype: AST
        :return: node
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def parse(self):
        return self.expr()


class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__.lower()
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception("No visit_{} method".format(type(node).__name__))


class Interpreter(NodeVisitor):
    """

    :param Parser parser:
    """

    def __init__(self, parser):
        self.parser = parser

    def visit_binop(self, node):
        op = OP_MAP.get(node.op.type, None)
        if op is None:
            raise SyntaxError(SYNTAX_ERROR_WRONG_OPERATION % node.op.type)
        return op(self.visit(node.left), self.visit(node.right))

    @staticmethod
    def visit_num(node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)
