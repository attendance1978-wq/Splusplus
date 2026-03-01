"""
S++ Interpreter v3 - Java-style Syntax
Features:
- class / func main
- arithmetic (+ - * /)
- booleans (true / false)
- if-else, while loops
- print syntax: print x = "..." ;
"""

import sys

# ============================================================================#
# TOKEN TYPES
# ============================================================================#
from enum import Enum

class TokenType(Enum):
    NUMBER = "NUMBER"
    STRING = "STRING"
    IDENTIFIER = "IDENTIFIER"
    BOOLEAN = "BOOLEAN"

    CLASS = "CLASS"
    FUNC = "FUNC"
    MAIN = "MAIN"
    RETURN = "RETURN"
    CALL = "CALL"

    IF = "IF"
    ELSE = "ELSE"
    WHILE = "WHILE"
    TRUE = "TRUE"
    FALSE = "FALSE"

    PLUS = "PLUS"
    MINUS = "MINUS"
    TIMES = "TIMES"
    DIVIDE = "DIVIDE"

    EQUAL = "EQUAL"
    NOTEQUAL = "NOTEQUAL"
    LESS = "LESS"
    GREATER = "GREATER"
    LE = "LE"
    GE = "GE"

    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    SEMICOLON = "SEMICOLON"
    COMMA = "COMMA"

    EOF = "EOF"

# ============================================================================#
# TOKEN
# ============================================================================#
class Token:
    def __init__(self, type, value, line, col):
        self.type = type
        self.value = value
        self.line = line
        self.col = col
    def __repr__(self):
        return f"{self.type}:{self.value}"

# ============================================================================#
# LEXER
# ============================================================================#
class Lexer:
    KEYWORDS = {
        "class": TokenType.CLASS,
        "func": TokenType.FUNC,
        "main": TokenType.MAIN,
        "return": TokenType.RETURN,
        "call": TokenType.CALL,
        "if": TokenType.IF,
        "else": TokenType.ELSE,
        "while": TokenType.WHILE,
        "true": TokenType.TRUE,
        "false": TokenType.FALSE
    }

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.col = 1
        self.current = text[0] if text else None

    def advance(self):
        if self.current == "\n":
            self.line +=1
            self.col = 1
        else:
            self.col +=1
        self.pos +=1
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
        while self.current and (self.current.isalnum() or self.current=="_"):
            word += self.current
            self.advance()
        lower = word.lower()
        if lower in self.KEYWORDS:
            return Token(self.KEYWORDS[lower], lower, self.line, start)
        return Token(TokenType.IDENTIFIER, word, self.line, start)

    def read_string(self):
        start = self.col
        self.advance()  # skip "
        s = ""
        while self.current and self.current != '"':
            s += self.current
            self.advance()
        if self.current != '"':
            raise Exception(f"Unterminated string at line {self.line}")
        self.advance()  # skip closing "
        return Token(TokenType.STRING, s, self.line, start)

    def next_token(self):
        while self.current:
            if self.current.isspace():
                self.skip_whitespace()
                continue
            if self.current.isdigit():
                return self.read_number()
            if self.current.isalpha() or self.current=="_":
                return self.read_word()
            if self.current == '"':
                return self.read_string()
            if self.current == '+':
                self.advance()
                return Token(TokenType.PLUS, '+', self.line, self.col)
            if self.current == '-':
                self.advance()
                return Token(TokenType.MINUS, '-', self.line, self.col)
            if self.current == '*':
                self.advance()
                return Token(TokenType.TIMES, '*', self.line, self.col)
            if self.current == '/':
                self.advance()
                return Token(TokenType.DIVIDE, '/', self.line, self.col)
            if self.current == '=':
                self.advance()
                if self.current == '=':
                    self.advance()
                    return Token(TokenType.EQUAL, "==", self.line, self.col)
                return Token(TokenType.EQUAL, '=', self.line, self.col)
            if self.current == '!':
                self.advance()
                if self.current == '=':
                    self.advance()
                    return Token(TokenType.NOTEQUAL, "!=", self.line, self.col)
            if self.current == '<':
                self.advance()
                if self.current == '=':
                    self.advance()
                    return Token(TokenType.LE, "<=", self.line, self.col)
                return Token(TokenType.LESS, '<', self.line, self.col)
            if self.current == '>':
                self.advance()
                if self.current == '=':
                    self.advance()
                    return Token(TokenType.GE, ">=", self.line, self.col)
                return Token(TokenType.GREATER, '>', self.line, self.col)
            if self.current == '{':
                self.advance()
                return Token(TokenType.LBRACE, '{', self.line, self.col)
            if self.current == '}':
                self.advance()
                return Token(TokenType.RBRACE, '}', self.line, self.col)
            if self.current == '(':
                self.advance()
                return Token(TokenType.LPAREN, '(', self.line, self.col)
            if self.current == ')':
                self.advance()
                return Token(TokenType.RPAREN, ')', self.line, self.col)
            if self.current == ';':
                self.advance()
                return Token(TokenType.SEMICOLON, ';', self.line, self.col)
            if self.current == ',':
                self.advance()
                return Token(TokenType.COMMA, ',', self.line, self.col)
            raise Exception(f"Unknown character: {self.current} at line {self.line}")
        return Token(TokenType.EOF, None, self.line, self.col)

# ============================================================================#
# AST NODES
# ============================================================================#
class AST: pass

class Program(AST):
    def __init__(self, classes):
        self.classes = classes

class ClassDef(AST):
    def __init__(self, name, methods):
        self.name = name
        self.methods = methods

class FuncDef(AST):
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

class Print(AST):
    def __init__(self, var_name, value):
        self.var_name = var_name
        self.value = value

class Set(AST):
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Call(AST):
    def __init__(self, name, args):
        self.name = name
        self.args = args

class If(AST):
    def __init__(self, condition, then_body, else_body=None):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

class While(AST):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class Number(AST):
    def __init__(self, value):
        self.value = value

class Boolean(AST):
    def __init__(self, value):
        self.value = value

class String(AST):
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

# ============================================================================#
# PARSER
# ============================================================================#
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current = lexer.next_token()

    def eat(self, type):
        if self.current.type == type:
            self.current = self.lexer.next_token()
        else:
            raise Exception(f"Expected {type} but got {self.current.type}")

    def parse(self):
        classes = []
        while self.current.type != TokenType.EOF:
            classes.append(self.parse_class())
        return Program(classes)

    def parse_class(self):
        self.eat(TokenType.CLASS)
        name = self.current.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.LBRACE)
        methods = []
        while self.current.type != TokenType.RBRACE:
            methods.append(self.parse_func())
        self.eat(TokenType.RBRACE)
        return ClassDef(name, methods)

    def parse_func(self):
        self.eat(TokenType.FUNC)
        name = self.current.value
        self.eat(TokenType.IDENTIFIER)

        params = []
        if self.current.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            while self.current.type != TokenType.RPAREN:
                params.append(self.current.value)
                self.eat(TokenType.IDENTIFIER)
                if self.current.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
            self.eat(TokenType.RPAREN)

        self.eat(TokenType.LBRACE)
        body = []
        while self.current.type != TokenType.RBRACE:
            body.append(self.parse_statement())
        self.eat(TokenType.RBRACE)

        return FuncDef(name, params, body)

    def parse_statement(self):
        if self.current.type == TokenType.IDENTIFIER:
            # Could be print
            if self.current.value.lower() == "print":
                return self.parse_print()
            else:
                raise Exception(f"Unknown statement: {self.current.value}")
        if self.current.type == TokenType.CALL:
            return self.parse_call()
        if self.current.type == TokenType.IF:
            return self.parse_if()
        if self.current.type == TokenType.WHILE:
            return self.parse_while()
        if self.current.type == TokenType.IDENTIFIER:
            return self.parse_set()
        raise Exception(f"Unknown statement at {self.current}")

    def parse_print(self):
        self.eat(TokenType.IDENTIFIER)  # print
        var_name = self.current.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.EQUAL)
        if self.current.type == TokenType.STRING:
            value = String(self.current.value)
            self.eat(TokenType.STRING)
        else:
            value = self.parse_expression()
        self.eat(TokenType.SEMICOLON)
        return Print(var_name, value)

    def parse_call(self):
        self.eat(TokenType.CALL)
        name = self.current.value
        self.eat(TokenType.IDENTIFIER)
        args = []
        if self.current.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            while self.current.type != TokenType.RPAREN:
                args.append(self.parse_expression())
                if self.current.type == TokenType.COMMA:
                    self.eat(TokenType.COMMA)
            self.eat(TokenType.RPAREN)
        self.eat(TokenType.SEMICOLON)
        return Call(name, args)

    def parse_if(self):
        self.eat(TokenType.IF)
        self.eat(TokenType.LPAREN)
        condition = self.parse_expression()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        then_body = []
        while self.current.type != TokenType.RBRACE:
            then_body.append(self.parse_statement())
        self.eat(TokenType.RBRACE)
        else_body = []
        if self.current.type == TokenType.ELSE:
            self.eat(TokenType.ELSE)
            self.eat(TokenType.LBRACE)
            while self.current.type != TokenType.RBRACE:
                else_body.append(self.parse_statement())
            self.eat(TokenType.RBRACE)
        return If(condition, then_body, else_body)

    def parse_while(self):
        self.eat(TokenType.WHILE)
        self.eat(TokenType.LPAREN)
        condition = self.parse_expression()
        self.eat(TokenType.RPAREN)
        self.eat(TokenType.LBRACE)
        body = []
        while self.current.type != TokenType.RBRACE:
            body.append(self.parse_statement())
        self.eat(TokenType.RBRACE)
        return While(condition, body)

    def parse_expression(self):
        node = self.parse_term()
        while self.current.type in (TokenType.PLUS, TokenType.MINUS):
            op = self.current.type
            self.eat(op)
            node = Binary(node, op, self.parse_term())
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current.type in (TokenType.TIMES, TokenType.DIVIDE):
            op = self.current.type
            self.eat(op)
            node = Binary(node, op, self.parse_factor())
        return node

    def parse_factor(self):
        token = self.current
        if token.type == TokenType.NUMBER:
            self.eat(TokenType.NUMBER)
            return Number(token.value)
        if token.type == TokenType.IDENTIFIER:
            self.eat(TokenType.IDENTIFIER)
            return Variable(token.value)
        if token.type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return Boolean(True)
        if token.type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return Boolean(False)
        if token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return node
        if token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return String(token.value)
        raise Exception(f"Unexpected token: {token}")

# ============================================================================#
# INTERPRETER
# ============================================================================#
class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.classes = {}

    def visit(self, node):
        method = "visit_" + type(node).__name__
        return getattr(self, method)(node)

    def visit_Program(self, node):
        for cls in node.classes:
            self.visit(cls)
        # execute main
        if "main" in self.functions:
            self.visit(self.functions["main"])

    def visit_ClassDef(self, node):
        for func in node.methods:
            self.functions[func.name] = func

    def visit_FuncDef(self, node):
        self.functions[node.name] = node

    def visit_Print(self, node):
        if isinstance(node.value, String):
            val = node.value.value
        else:
            val = self.visit(node.value)
        self.variables[node.var_name] = val
        print(val)

    def visit_Call(self, node):
        if node.name not in self.functions:
            raise Exception(f"Function {node.name} not found")
        func = self.functions[node.name]
        old_vars = self.variables.copy()
        for param, arg in zip(func.params, node.args):
            self.variables[param] = self.visit(arg)
        for stmt in func.body:
            self.visit(stmt)
        self.variables = old_vars

    def visit_Number(self, node):
        return node.value

    def visit_String(self, node):
        return node.value

    def visit_Boolean(self, node):
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
        if node.op == TokenType.TIMES:
            return left * right
        if node.op == TokenType.DIVIDE:
            return left / right
        return None

    def visit_If(self, node):
        if self.visit(node.condition):
            for stmt in node.then_body:
                self.visit(stmt)
        elif node.else_body:
            for stmt in node.else_body:
                self.visit(stmt)

    def visit_While(self, node):
        while self.visit(node.condition):
            for stmt in node.body:
                self.visit(stmt)

# ============================================================================#
# RUN
# ============================================================================#
def run(code):
    lexer = Lexer(code)
    parser = Parser(lexer)
    tree = parser.parse()
    interpreter = Interpreter()
    interpreter.visit(tree)

# ============================================================================#
# CLI ENTRY
# ============================================================================#
if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1],"r") as f:
            code = f.read()
        run(code)
    else:
        print("S++ Interpreter v3 - Java-style syntax")
        print("Type STOP; to run\n")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "STOP;":
                break
            lines.append(line)
        run("\n".join(lines))
