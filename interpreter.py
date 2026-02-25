"""
S++ Language Interpreter
An English-like programming language with minimal symbols (only comma and period)
"""

import re
import sys
from enum import Enum
from typing import Any, Dict, List, Optional, Union

# ============================================================================
# LEXER
# ============================================================================

class TokenType(Enum):
    # Literals
    NUMBER = "NUMBER"
    STRING = "STRING"
    
    # Keywords
    SET = "SET"
    TO = "TO"
    PRINT = "PRINT"
    WRITE = "WRITE"
    ASK = "ASK"
    AND_STORE_IN = "AND_STORE_IN"
    IF = "IF"
    THEN = "THEN"
    OTHERWISE = "OTHERWISE"
    END = "END"
    REPEAT = "REPEAT"
    WHILE = "WHILE"
    TIMES = "TIMES"
    FOR = "FOR"
    EACH = "EACH"
    IN = "IN"
    DEFINE = "DEFINE"
    WITH = "WITH"
    CALL = "CALL"
    RETURN = "RETURN"
    
    # Operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    TIMES_OP = "TIMES_OP"
    DIVIDED_BY = "DIVIDED_BY"
    EQUALS = "EQUALS"
    IS_GREATER_THAN = "IS_GREATER_THAN"
    IS_LESS_THAN = "IS_LESS_THAN"
    IS_EQUAL_TO = "IS_EQUAL_TO"
    OR = "OR"
    NOT = "NOT"
    
    # Symbols
    COMMA = "COMMA"
    PERIOD = "PERIOD"
    
    # Special
    IDENTIFIER = "IDENTIFIER"
    EOF = "EOF"

class Token:
    def __init__(self, token_type: TokenType, value: Any, line: int, column: int):
        self.type = token_type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, {self.line}:{self.column})"

class Lexer:
    KEYWORDS = {
        'set': TokenType.SET,
        'to': TokenType.TO,
        'print': TokenType.PRINT,
        'write': TokenType.WRITE,
        'ask': TokenType.ASK,
        'and': TokenType.OR,  # Used in "and" conditions
        'store': TokenType.AND_STORE_IN,
        'in': TokenType.IN,
        'if': TokenType.IF,
        'then': TokenType.THEN,
        'otherwise': TokenType.OTHERWISE,
        'end': TokenType.END,
        'repeat': TokenType.REPEAT,
        'while': TokenType.WHILE,
        'times': TokenType.TIMES,
        'for': TokenType.FOR,
        'each': TokenType.EACH,
        'define': TokenType.DEFINE,
        'with': TokenType.WITH,
        'call': TokenType.CALL,
        'return': TokenType.RETURN,
        'plus': TokenType.PLUS,
        'minus': TokenType.MINUS,
        'times': TokenType.TIMES_OP,
        'divided': TokenType.DIVIDED_BY,
        'equals': TokenType.EQUALS,
        'or': TokenType.OR,
        'not': TokenType.NOT,
    }
    
    def __init__(self, text: str):
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.text[0] if text else None
    
    def advance(self):
        if self.current_char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
    
    def peek(self, offset: int = 1) -> Optional[str]:
        peek_pos = self.pos + offset
        if peek_pos >= len(self.text):
            return None
        return self.text[peek_pos]
    
    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()
    
    def skip_comment(self):
        if self.current_char == '/' and self.peek() == '/':
            while self.current_char and self.current_char != '\n':
                self.advance()
    
    def read_number(self) -> Token:
        line, col = self.line, self.column
        num_str = ''
        
        while self.current_char and self.current_char.isdigit():
            num_str += self.current_char
            self.advance()
        
        if self.current_char == '.' and self.peek() and self.peek().isdigit():
            num_str += '.'
            self.advance()
            while self.current_char and self.current_char.isdigit():
                num_str += self.current_char
                self.advance()
        
        return Token(TokenType.NUMBER, float(num_str) if '.' in num_str else int(num_str), line, col)
    
    def read_word(self) -> Token:
        line, col = self.line, self.column
        word = ''
        
        while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
            word += self.current_char
            self.advance()
        
        word_lower = word.lower()
        
        # Special handling for "divided" - check if followed by "by"
        if word_lower == 'divided':
            # Save current position
            saved_pos = self.pos
            saved_char = self.current_char
            saved_line, saved_col = self.line, self.column
            
            # Try to peek ahead for "by"
            self.skip_whitespace()
            temp_word = ''
            while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
                temp_word += self.current_char
                self.advance()
            
            if temp_word.lower() == 'by':
                # Consume the "by" as part of the operator
                return Token(TokenType.DIVIDED_BY, 'divided by', line, col)
            else:
                # Reset and treat "divided" as an identifier
                self.pos = saved_pos
                self.current_char = saved_char
                self.line = saved_line
                self.column = saved_col
                word_lower = 'divided'
        
        # Similar handling for "is greater than"
        if word_lower == 'is':
            saved_pos = self.pos
            saved_char = self.current_char
            saved_line, saved_col = self.line, self.column
            
            self.skip_whitespace()
            temp_word = ''
            while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
                temp_word += self.current_char
                self.advance()
            
            if temp_word.lower() == 'greater':
                # Check for "than"
                self.skip_whitespace()
                temp_word2 = ''
                while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
                    temp_word2 += self.current_char
                    self.advance()
                
                if temp_word2.lower() == 'than':
                    return Token(TokenType.IS_GREATER_THAN, 'is greater than', line, col)
            elif temp_word.lower() == 'less':
                # Check for "than"
                self.skip_whitespace()
                temp_word2 = ''
                while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
                    temp_word2 += self.current_char
                    self.advance()
                
                if temp_word2.lower() == 'than':
                    return Token(TokenType.IS_LESS_THAN, 'is less than', line, col)
            
            # Reset if not a multi-word operator
            self.pos = saved_pos
            self.current_char = saved_char
            self.line = saved_line
            self.column = saved_col
        
        if word_lower in self.KEYWORDS:
            token_type = self.KEYWORDS[word_lower]
        else:
            token_type = TokenType.IDENTIFIER
        
        return Token(token_type, word, line, col)
    
    def get_next_token(self) -> Token:
        while self.current_char:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char == '/' and self.peek() == '/':
                self.skip_comment()
                continue
            
            if self.current_char.isdigit():
                return self.read_number()
            
            if self.current_char.isalpha() or self.current_char == '_':
                return self.read_word()
            
            if self.current_char == ',':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.COMMA, ',', line, col)
            
            if self.current_char == '.':
                line, col = self.line, self.column
                self.advance()
                return Token(TokenType.PERIOD, '.', line, col)
            
            raise Exception(f"Invalid character '{self.current_char}' at {self.line}:{self.column}")
        
        return Token(TokenType.EOF, None, self.line, self.column)

# ============================================================================
# AST NODES
# ============================================================================

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements: List[ASTNode]):
        self.statements = statements

class SetStatement(ASTNode):
    def __init__(self, var_name: str, value: ASTNode):
        self.var_name = var_name
        self.value = value

class PrintStatement(ASTNode):
    def __init__(self, expression: ASTNode):
        self.expression = expression

class AskStatement(ASTNode):
    def __init__(self, prompt: str, var_name: str):
        self.prompt = prompt
        self.var_name = var_name

class IfStatement(ASTNode):
    def __init__(self, condition: ASTNode, then_body: List[ASTNode], else_body: Optional[List[ASTNode]]):
        self.condition = condition
        self.then_body = then_body
        self.else_body = else_body

class RepeatWhileStatement(ASTNode):
    def __init__(self, condition: ASTNode, body: List[ASTNode]):
        self.condition = condition
        self.body = body

class RepeatTimesStatement(ASTNode):
    def __init__(self, count: ASTNode, body: List[ASTNode]):
        self.count = count
        self.body = body

class ForEachStatement(ASTNode):
    def __init__(self, item_name: str, list_expr: ASTNode, body: List[ASTNode]):
        self.item_name = item_name
        self.list_expr = list_expr
        self.body = body

class FunctionDef(ASTNode):
    def __init__(self, name: str, params: List[str], body: List[ASTNode]):
        self.name = name
        self.params = params
        self.body = body

class FunctionCall(ASTNode):
    def __init__(self, name: str, args: List[ASTNode]):
        self.name = name
        self.args = args

class ReturnStatement(ASTNode):
    def __init__(self, value: Optional[ASTNode]):
        self.value = value

class BinaryOp(ASTNode):
    def __init__(self, left: ASTNode, op: Token, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(ASTNode):
    def __init__(self, op: Token, expr: ASTNode):
        self.op = op
        self.expr = expr

class Literal(ASTNode):
    def __init__(self, value: Any):
        self.value = value

class Variable(ASTNode):
    def __init__(self, name: str):
        self.name = name
        self.is_literal_if_undefined = False  # Flag for print context

class ListLiteral(ASTNode):
    def __init__(self, items: List[ASTNode]):
        self.items = items

# ============================================================================
# PARSER
# ============================================================================

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
    
    def eat(self, token_type: TokenType):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise Exception(f"Expected {token_type}, got {self.current_token.type}")
    
    def parse(self) -> Program:
        statements = []
        while self.current_token.type != TokenType.EOF:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def parse_statement(self) -> Optional[ASTNode]:
        if self.current_token.type == TokenType.SET:
            return self.parse_set_statement()
        elif self.current_token.type == TokenType.PRINT:
            return self.parse_print_statement()
        elif self.current_token.type == TokenType.WRITE:
            return self.parse_print_statement()
        elif self.current_token.type == TokenType.ASK:
            return self.parse_ask_statement()
        elif self.current_token.type == TokenType.IF:
            return self.parse_if_statement()
        elif self.current_token.type == TokenType.REPEAT:
            return self.parse_repeat_statement()
        elif self.current_token.type == TokenType.FOR:
            return self.parse_for_statement()
        elif self.current_token.type == TokenType.DEFINE:
            return self.parse_function_def()
        elif self.current_token.type == TokenType.CALL:
            return self.parse_function_call()
        elif self.current_token.type == TokenType.RETURN:
            return self.parse_return_statement()
        else:
            return None
    
    def parse_set_statement(self) -> SetStatement:
        self.eat(TokenType.SET)
        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.TO)
        value = self.parse_set_expression()
        self.eat(TokenType.PERIOD)
        return SetStatement(var_name, value)
    
    def parse_set_expression(self) -> ASTNode:
        """Parse expression in a set context, allowing undefined identifiers as literals"""
        expr = self.parse_expression()
        # Enable literal fallback for all variables in this expression
        self._mark_fallback_to_literal(expr)
        return expr
    
    def _mark_fallback_to_literal(self, node: ASTNode):
        """Recursively mark all Variable nodes to fallback to literal if undefined"""
        if isinstance(node, Variable):
            node.is_literal_if_undefined = True
        elif isinstance(node, BinaryOp):
            self._mark_fallback_to_literal(node.left)
            self._mark_fallback_to_literal(node.right)
        elif isinstance(node, UnaryOp):
            self._mark_fallback_to_literal(node.expr)
    
    def parse_print_statement(self) -> PrintStatement:
        self.eat(self.current_token.type)  # PRINT or WRITE
        
        # Collect everything until period, treating most things as a phrase
        words = []
        
        while self.current_token.type != TokenType.PERIOD and self.current_token.type != TokenType.EOF:
            # Stop at operators that would indicate this is an expression
            if self.current_token.type in [TokenType.PLUS, TokenType.MINUS, TokenType.TIMES_OP, TokenType.DIVIDED_BY]:
                # This is an operation on previous words
                if len(words) > 0:
                    # Parse the first word as a variable/number and the rest as expression
                    first_val = words[0]
                    if first_val.isdigit() or (first_val[0].isdigit() if first_val else False):
                        left = Literal(int(first_val))
                    else:
                        left = Variable(first_val)
                        left.is_literal_if_undefined = True
                    
                    # Now parse operators
                    while self.current_token.type in [TokenType.PLUS, TokenType.MINUS, TokenType.TIMES_OP, TokenType.DIVIDED_BY]:
                        op = self.current_token
                        self.eat(self.current_token.type)
                        
                        if self.current_token.type == TokenType.NUMBER:
                            right = Literal(self.current_token.value)
                            self.eat(TokenType.NUMBER)
                        elif self.current_token.type == TokenType.IDENTIFIER:
                            right = Variable(self.current_token.value)
                            right.is_literal_if_undefined = True
                            self.eat(TokenType.IDENTIFIER)
                        else:
                            raise Exception(f"Expected operand after operator")
                        
                        left = BinaryOp(left, op, right)
                    
                    self.eat(TokenType.PERIOD)
                    return PrintStatement(left)
                else:
                    raise Exception("No left operand for expression")
            elif self.current_token.type in [TokenType.IDENTIFIER, TokenType.NUMBER]:
                words.append(str(self.current_token.value))
                self.eat(self.current_token.type)
            else:
                # It's some other keyword... treat it as part of the phrase
                if self.current_token.type == TokenType.TO:
                    words.append('to')
                    self.eat(TokenType.TO)
                elif self.current_token.type == TokenType.AND_STORE_IN:
                    words.append('and store in')
                    self.eat(TokenType.AND_STORE_IN)
                else:
                    # For other keywords, try to treat as part of phrase
                    words.append(self.current_token.value if self.current_token.value else self.current_token.type.name.lower())
                    self.eat(self.current_token.type)
        
        self.eat(TokenType.PERIOD)
        
        if len(words) == 0:
            raise Exception("No expression after print statement")
        elif len(words) == 1:
            # Single word - could be variable or literal
            token_val = words[0]
            var_node = Variable(token_val)
            var_node.is_literal_if_undefined = True
            return PrintStatement(var_node)
        else:
            # Multiple words - treat as phrase
            phrase = ' '.join(words)
            return PrintStatement(Literal(phrase))
    
    def parse_ask_statement(self) -> AskStatement:
        self.eat(TokenType.ASK)
        prompt = self.parse_string_phrase()
        self.eat(TokenType.AND_STORE_IN)
        var_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.PERIOD)
        return AskStatement(prompt, var_name)
    
    def parse_if_statement(self) -> IfStatement:
        self.eat(TokenType.IF)
        condition = self.parse_expression()
        self.eat(TokenType.THEN)
        then_body = self.parse_block()
        
        else_body = None
        if self.current_token.type == TokenType.OTHERWISE:
            self.eat(TokenType.OTHERWISE)
            else_body = self.parse_block()
        
        self.eat(TokenType.END)
        self.eat(TokenType.PERIOD)
        return IfStatement(condition, then_body, else_body)
    
    def parse_repeat_statement(self) -> Union[RepeatWhileStatement, RepeatTimesStatement]:
        self.eat(TokenType.REPEAT)
        
        if self.current_token.type == TokenType.WHILE:
            self.eat(TokenType.WHILE)
            condition = self.parse_expression()
            body = self.parse_block()
            self.eat(TokenType.END)
            self.eat(TokenType.PERIOD)
            return RepeatWhileStatement(condition, body)
        else:
            # Parse count - but be careful not to consume 'times'
            # We only want primary expressions here, not multiplication
            if self.current_token.type == TokenType.NUMBER:
                count = Literal(self.current_token.value)
                self.eat(TokenType.NUMBER)
            elif self.current_token.type == TokenType.IDENTIFIER:
                count = Variable(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
            else:
                count = self.parse_primary()
            
            self.eat(TokenType.TIMES_OP)  # 'times' keyword
            body = self.parse_block()
            self.eat(TokenType.END)
            self.eat(TokenType.PERIOD)
            return RepeatTimesStatement(count, body)
    
    def parse_for_statement(self) -> ForEachStatement:
        self.eat(TokenType.FOR)
        self.eat(TokenType.EACH)
        item_name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        self.eat(TokenType.IN)
        list_expr = self.parse_expression()
        body = self.parse_block()
        self.eat(TokenType.END)
        self.eat(TokenType.PERIOD)
        return ForEachStatement(item_name, list_expr, body)
    
    def parse_function_def(self) -> FunctionDef:
        self.eat(TokenType.DEFINE)
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        params = []
        if self.current_token.type == TokenType.WITH:
            self.eat(TokenType.WITH)
            params.append(self.current_token.value)
            self.eat(TokenType.IDENTIFIER)
            
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                params.append(self.current_token.value)
                self.eat(TokenType.IDENTIFIER)
        
        body = self.parse_block()
        self.eat(TokenType.END)
        self.eat(TokenType.PERIOD)
        return FunctionDef(name, params, body)
    
    def parse_function_call(self) -> FunctionCall:
        self.eat(TokenType.CALL)
        name = self.current_token.value
        self.eat(TokenType.IDENTIFIER)
        
        args = []
        if self.current_token.type == TokenType.WITH:
            self.eat(TokenType.WITH)
            args.append(self.parse_expression())
            
            while self.current_token.type == TokenType.COMMA:
                self.eat(TokenType.COMMA)
                args.append(self.parse_expression())
        
        return FunctionCall(name, args)
    
    def parse_return_statement(self) -> ReturnStatement:
        self.eat(TokenType.RETURN)
        value = None
        if self.current_token.type != TokenType.PERIOD:
            value = self.parse_expression()
        self.eat(TokenType.PERIOD)
        return ReturnStatement(value)
    
    def parse_block(self) -> List[ASTNode]:
        statements = []
        while self.current_token.type not in [TokenType.END, TokenType.OTHERWISE, TokenType.EOF]:
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        return statements
    
    def parse_expression(self) -> ASTNode:
        return self.parse_or_expr()
    
    def parse_or_expr(self) -> ASTNode:
        left = self.parse_and_expr()
        
        while self.current_token.type == TokenType.OR:
            op = self.current_token
            self.eat(TokenType.OR)
            right = self.parse_and_expr()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_and_expr(self) -> ASTNode:
        left = self.parse_comparison()
        
        while self.current_token.type == TokenType.OR and self.lexer.text[self.lexer.pos-5:self.lexer.pos].lower().endswith('and'):
            op = self.current_token
            self.eat(TokenType.OR)
            right = self.parse_comparison()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_comparison(self) -> ASTNode:
        left = self.parse_addition()
        
        while self.current_token.type in [TokenType.EQUALS, TokenType.IS_GREATER_THAN, TokenType.IS_LESS_THAN]:
            op = self.current_token
            self.eat(self.current_token.type)
            right = self.parse_addition()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_addition(self) -> ASTNode:
        left = self.parse_multiplication()
        
        while self.current_token.type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token
            self.eat(self.current_token.type)
            right = self.parse_multiplication()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplication(self) -> ASTNode:
        left = self.parse_unary()
        
        while self.current_token.type in [TokenType.TIMES_OP, TokenType.DIVIDED_BY]:
            op = self.current_token
            self.eat(self.current_token.type)
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_unary(self) -> ASTNode:
        if self.current_token.type == TokenType.NOT:
            op = self.current_token
            self.eat(TokenType.NOT)
            expr = self.parse_unary()
            return UnaryOp(op, expr)
        
        return self.parse_primary()
    
    def parse_primary(self) -> ASTNode:
        if self.current_token.type == TokenType.NUMBER:
            value = self.current_token.value
            self.eat(TokenType.NUMBER)
            return Literal(value)
        
        elif self.current_token.type == TokenType.IDENTIFIER:
            name = self.current_token.value
            self.eat(TokenType.IDENTIFIER)
            
            # Check for list literal or function call
            if self.current_token.type == TokenType.COMMA or (self.current_token.type != TokenType.PERIOD and self.current_token.type != TokenType.COMMA):
                return Variable(name)
            
            return Variable(name)
        
        elif self.current_token.type == TokenType.CALL:
            return self.parse_function_call()
        
        else:
            raise Exception(f"Unexpected token: {self.current_token}")
    
    def parse_string_phrase(self) -> str:
        words = []
        while self.current_token.type in [TokenType.IDENTIFIER, TokenType.NUMBER]:
            words.append(str(self.current_token.value))
            self.eat(self.current_token.type)
        return ' '.join(words)

# ============================================================================
# INTERPRETER
# ============================================================================

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
    
    def visit(self, node: ASTNode) -> Any:
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.visit_generic)
        return method(node)
    
    def visit_generic(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')
    
    def visit_Program(self, node: Program) -> Any:
        result = None
        for stmt in node.statements:
            result = self.visit(stmt)
        return result
    
    def visit_SetStatement(self, node: SetStatement) -> Any:
        value = self.visit(node.value)
        self.variables[node.var_name] = value
        return value
    
    def visit_PrintStatement(self, node: PrintStatement) -> Any:
        value = self.visit(node.expression)
        print(self.format_output(value))
        return value
    
    def visit_AskStatement(self, node: AskStatement) -> Any:
        value = input(node.prompt + " ")
        try:
            self.variables[node.var_name] = int(value)
        except ValueError:
            try:
                self.variables[node.var_name] = float(value)
            except ValueError:
                self.variables[node.var_name] = value
        return self.variables[node.var_name]
    
    def visit_IfStatement(self, node: IfStatement) -> Any:
        condition = self.visit(node.condition)
        if self.is_truthy(condition):
            for stmt in node.then_body:
                self.visit(stmt)
        elif node.else_body:
            for stmt in node.else_body:
                self.visit(stmt)
    
    def visit_RepeatWhileStatement(self, node: RepeatWhileStatement) -> Any:
        while self.is_truthy(self.visit(node.condition)):
            for stmt in node.body:
                self.visit(stmt)
    
    def visit_RepeatTimesStatement(self, node: RepeatTimesStatement) -> Any:
        count = int(self.visit(node.count))
        for _ in range(count):
            for stmt in node.body:
                self.visit(stmt)
    
    def visit_ForEachStatement(self, node: ForEachStatement) -> Any:
        items = self.visit(node.list_expr)
        if not isinstance(items, list):
            items = [items]
        
        for item in items:
            self.variables[node.item_name] = item
            for stmt in node.body:
                self.visit(stmt)
    
    def visit_FunctionDef(self, node: FunctionDef) -> Any:
        self.functions[node.name] = node
    
    def visit_FunctionCall(self, node: FunctionCall) -> Any:
        if node.name not in self.functions:
            raise Exception(f"Function '{node.name}' not defined")
        
        func_def = self.functions[node.name]
        args = [self.visit(arg) for arg in node.args]
        
        # Create local scope
        old_vars = self.variables.copy()
        
        # Bind parameters
        for i, param in enumerate(func_def.params):
            if i < len(args):
                self.variables[param] = args[i]
        
        # Execute function body
        result = None
        try:
            for stmt in func_def.body:
                self.visit(stmt)
        except ReturnValue as ret:
            result = ret.value
        
        # Restore scope
        self.variables = old_vars
        
        return result
    
    def visit_ReturnStatement(self, node: ReturnStatement) -> Any:
        value = self.visit(node.value) if node.value else None
        raise ReturnValue(value)
    
    def visit_BinaryOp(self, node: BinaryOp) -> Any:
        left = self.visit(node.left)
        right = self.visit(node.right)
        
        if node.op.type == TokenType.PLUS:
            return left + right
        elif node.op.type == TokenType.MINUS:
            return left - right
        elif node.op.type == TokenType.TIMES_OP:
            return left * right
        elif node.op.type == TokenType.DIVIDED_BY:
            return left / right if right != 0 else 0
        elif node.op.type == TokenType.EQUALS:
            return left == right
        elif node.op.type == TokenType.IS_GREATER_THAN:
            return left > right
        elif node.op.type == TokenType.IS_LESS_THAN:
            return left < right
        elif node.op.type == TokenType.OR:
            return self.is_truthy(left) or self.is_truthy(right)
    
    def visit_UnaryOp(self, node: UnaryOp) -> Any:
        expr = self.visit(node.expr)
        
        if node.op.type == TokenType.NOT:
            return not self.is_truthy(expr)
    
    def visit_Literal(self, node: Literal) -> Any:
        return node.value
    
    def visit_Variable(self, node: Variable) -> Any:
        if node.name not in self.variables:
            # If this is a print context and variable is undefined, treat as literal
            if hasattr(node, 'is_literal_if_undefined') and node.is_literal_if_undefined:
                return node.name
            raise Exception(f"Variable '{node.name}' not defined")
        return self.variables[node.name]
    
    def visit_ListLiteral(self, node: ListLiteral) -> Any:
        return [self.visit(item) for item in node.items]
    
    def is_truthy(self, value: Any) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return value.lower() not in ['', 'false', 'no']
        if isinstance(value, list):
            return len(value) > 0
        return bool(value)
    
    def format_output(self, value: Any) -> str:
        if isinstance(value, list):
            return ', '.join(str(item) for item in value)
        return str(value)

# ============================================================================
# MAIN
# ============================================================================

def run_program(code: str):
    try:
        lexer = Lexer(code)
        parser = Parser(lexer)
        ast = parser.parse()
        interpreter = Interpreter()
        interpreter.visit(ast)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            code = f.read()
        run_program(code)
    else:
        print("S++ Language Interpreter")
        print("========================")
        print("Enter code (type 'STOP.' on a new line to execute):")
        lines = []
        while True:
            line = input()
            if line.strip() == 'STOP.':
                break
            lines.append(line)
        
        code = '\n'.join(lines)
        run_program(code)
