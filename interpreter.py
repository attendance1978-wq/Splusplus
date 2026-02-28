"""
S++ Language Interpreter v2
File: interpreter.py

Features:
- main class
- class support
- func support
- automatic main execution
- variables
- math operations
- print/write
- function calls
"""

import sys
from enum import Enum
from typing import Any, Dict, List


# ============================================================================
# TOKEN TYPES
# ============================================================================

class TokenType(Enum):

    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"

    SET = "SET"
    TO = "TO"

    PRINT = "PRINT"
    WRITE = "WRITE"

    CLASS = "CLASS"
    FUNC = "FUNC"
    MAIN = "MAIN"
    END = "END"

    CALL = "CALL"
    RETURN = "RETURN"

    PLUS = "PLUS"
    MINUS = "MINUS"
    TIMES = "TIMES"
    DIVIDED = "DIVIDED"

    PERIOD = "PERIOD"
    COMMA = "COMMA"

    EOF = "EOF"


# ============================================================================
# TOKEN
# ============================================================================

class Token:

    def __init__(self, type, value, line, col):
        self.type = type
        self.value = value
        self.line = line
        self.col = col

    def __repr__(self):
        return f"{self.type}:{self.value}"


# ============================================================================
# LEXER
# ============================================================================

class Lexer:

    KEYWORDS = {

        "set": TokenType.SET,
        "to": TokenType.TO,

        "print": TokenType.PRINT,
        "write": TokenType.WRITE,

        "class": TokenType.CLASS,
        "func": TokenType.FUNC,
        "main": TokenType.MAIN,
        "end": TokenType.END,

        "call": TokenType.CALL,
        "return": TokenType.RETURN,

        "plus": TokenType.PLUS,
        "minus": TokenType.MINUS,
        "times": TokenType.TIMES,
        "divided": TokenType.DIVIDED,
    }

    def __init__(self, text):

        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1

        self.current = text[0] if text else None


    def advance(self):

        if self.current == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1

        self.pos += 1

        if self.pos >= len(self.text):
            self.current = None
        else:
            self.current = self.text[self.pos]


    def skip_whitespace(self):

        while self.current and self.current.isspace():
            self.advance()


    def read_number(self):

        start = self.col
        num = ""

        while self.current and self.current.isdigit():
            num += self.current
            self.advance()

        return Token(TokenType.NUMBER, int(num), self.line, start)


    def read_word(self):

        start = self.col
        word = ""

        while self.current and (self.current.isalnum() or self.current == "_"):
            word += self.current
            self.advance()

        lower = word.lower()

        if lower in self.KEYWORDS:
            return Token(self.KEYWORDS[lower], lower, self.line, start)

        return Token(TokenType.IDENTIFIER, word, self.line, start)


    def next_token(self):

        while self.current:

            if self.current.isspace():
                self.skip_whitespace()
                continue

            if self.current.isdigit():
                return self.read_number()

            if self.current.isalpha():
                return self.read_word()

            if self.current == ".":
                self.advance()
                return Token(TokenType.PERIOD, ".", self.line, self.col)

            if self.current == ",":
                self.advance()
                return Token(TokenType.COMMA, ",", self.line, self.col)

            raise Exception(f"Invalid character: {self.current}")

        return Token(TokenType.EOF, None, self.line, self.col)


# ============================================================================
# AST NODES
# ============================================================================

class AST: pass


class Program(AST):

    def __init__(self, statements):
        self.statements = statements


class ClassDef(AST):

    def __init__(self, name, methods):
        self.name = name
        self.methods = methods


class FuncDef(AST):

    def __init__(self, name, body):
        self.name = name
        self.body = body


class Print(AST):

    def __init__(self, value):
        self.value = value


class Set(AST):

    def __init__(self, name, value):
        self.name = name
        self.value = value


class Call(AST):

    def __init__(self, name):
        self.name = name


class Number(AST):

    def __init__(self, value):
        self.value = value


class Variable(AST):

    def __init__(self, name):
        self.name = name


class Binary(AST):

    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


# ============================================================================
# PARSER
# ============================================================================

class Parser:

    def __init__(self, lexer):

        self.lexer = lexer
        self.current = lexer.next_token()


    def eat(self, type):

        if self.current.type == type:
            self.current = self.lexer.next_token()
        else:
            raise Exception(f"Expected {type}, got {self.current.type}")


    def parse(self):

        statements = []

        while self.current.type != TokenType.EOF:
            statements.append(self.parse_statement())

        return Program(statements)


    def parse_statement(self):

        if self.current.type == TokenType.MAIN:
            return self.parse_main_class()

        if self.current.type == TokenType.CLASS:
            return self.parse_class()

        if self.current.type == TokenType.FUNC:
            return self.parse_func()

        if self.current.type in (TokenType.PRINT, TokenType.WRITE):
            return self.parse_print()

        if self.current.type == TokenType.SET:
            return self.parse_set()

        if self.current.type == TokenType.CALL:
            return self.parse_call()

        raise Exception(f"Invalid statement at {self.current}")


    def parse_main_class(self):

        self.eat(TokenType.MAIN)
        self.eat(TokenType.CLASS)
        self.eat(TokenType.PERIOD)

        methods = []

        while self.current.type != TokenType.END:
            methods.append(self.parse_func())

        self.eat(TokenType.END)
        self.eat(TokenType.CLASS)
        self.eat(TokenType.PERIOD)

        return ClassDef("main", methods)


    def parse_class(self):

        self.eat(TokenType.CLASS)

        name = self.current.value
        self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.PERIOD)

        methods = []

        while self.current.type != TokenType.END:
            methods.append(self.parse_func())

        self.eat(TokenType.END)
        self.eat(TokenType.CLASS)
        self.eat(TokenType.PERIOD)

        return ClassDef(name, methods)


    def parse_func(self):

        self.eat(TokenType.FUNC)

        if self.current.type == TokenType.MAIN:
            name = "main"
            self.eat(TokenType.MAIN)
        else:
            name = self.current.value
            self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.PERIOD)

        body = []

        while self.current.type != TokenType.END:
            body.append(self.parse_statement())

        self.eat(TokenType.END)
        self.eat(TokenType.FUNC)
        self.eat(TokenType.PERIOD)

        return FuncDef(name, body)


    def parse_print(self):

        self.eat(self.current.type)

        value = self.current.value
        self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.PERIOD)

        return Print(value)


    def parse_set(self):

        self.eat(TokenType.SET)

        name = self.current.value
        self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.TO)

        value = self.parse_expression()

        self.eat(TokenType.PERIOD)

        return Set(name, value)


    def parse_call(self):

        self.eat(TokenType.CALL)

        name = self.current.value
        self.eat(TokenType.IDENTIFIER)

        self.eat(TokenType.PERIOD)

        return Call(name)


    def parse_expression(self):

        left = self.parse_term()

        while self.current.type in (TokenType.PLUS, TokenType.MINUS):

            op = self.current.type
            self.eat(op)

            right = self.parse_term()

            left = Binary(left, op, right)

        return left


    def parse_term(self):

        token = self.current

        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(token.value)

        if token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Variable(token.value)

        raise Exception("Invalid expression")


# ============================================================================
# INTERPRETER
# ============================================================================

class Interpreter:

    def __init__(self):

        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, FuncDef] = {}
        self.classes: Dict[str, ClassDef] = {}


    def visit(self, node):

        method = "visit_" + type(node).__name__
        return getattr(self, method)(node)


    def visit_Program(self, node):

        for stmt in node.statements:
            self.visit(stmt)

        if "main" in self.functions:
            self.visit(self.functions["main"])


    def visit_ClassDef(self, node):

        self.classes[node.name] = node

        for func in node.methods:
            self.functions[func.name] = func


    def visit_FuncDef(self, node):

        for stmt in node.body:
            self.visit(stmt)


    def visit_Print(self, node):

        if node.value in self.variables:
            print(self.variables[node.value])
        else:
            print(node.value)


    def visit_Set(self, node):

        value = self.visit(node.value)
        self.variables[node.name] = value


    def visit_Call(self, node):

        if node.name in self.functions:
            self.visit(self.functions[node.name])
        else:
            raise Exception(f"Function '{node.name}' not found")


    def visit_Number(self, node):
        return node.value


    def visit_Variable(self, node):

        if node.name in self.variables:
            return self.variables[node.name]

        return node.name


    def visit_Binary(self, node):

        left = self.visit(node.left)
        right = self.visit(node.right)

        if node.op == TokenType.PLUS:
            return left + right

        if node.op == TokenType.MINUS:
            return left - right

        raise Exception("Invalid math operator")


# ============================================================================
# RUN
# ============================================================================

def run(code: str):

    lexer = Lexer(code)
    parser = Parser(lexer)
    tree = parser.parse()

    interpreter = Interpreter()
    interpreter.visit(tree)


# ============================================================================
# CLI ENTRY
# ============================================================================

if __name__ == "__main__":

    if len(sys.argv) > 1:

        with open(sys.argv[1], "r") as f:
            code = f.read()

        run(code)

    else:

        print("S++ Interpreter v2")
        print("Type STOP. to run\n")

        lines = []

        while True:

            line = input()

            if line.strip() == "STOP.":
                break

            lines.append(line)

        run("\n".join(lines))
