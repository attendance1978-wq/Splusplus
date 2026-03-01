# 📖 S++ Language Specification (Java-style)

## 🎯 Overview
S++ (Simplified Programming Plus) is an English-like programming language designed for ease of use and readability. It uses **Java-style classes and functions**, minimal punctuation, and natural English keywords, making it beginner-friendly.

---

## 1. ⌨️ Syntax Structure

### Class and Function
```
class ProjectName {
func main() {
statements;
}
}
```
- All code runs inside **classes**  
- Entry point is `func main()`  
- Functions are defined with `func`  

---

## 2. 📦 Variables

### 📝 Declaration and Assignment
Variables are created using the `set` keyword:


set variable_name = value;


### 🎨 Data Types
S++ supports multiple data types:
- **#️⃣ Numbers**: Integers and floats (`10`, `3.14`)
- **📝 Strings**: Text in double quotes (`"hello world"`)
- **✓ Booleans**: `true` / `false`
- **📋 Lists**: Comma-separated values (`1,2,3`)

### Examples
```
set age = 25;
set name = "John";
set message = "Hello world";
set numbers = 1,2,3,4,5;
set total = 0;

```
---
```
## 3. 📢 Input and Output

### 🖨️ Print
Display values to the console:


print x = "Hello World";
print total = a + b;


### ⌨️ Input (Ask)
Get user input:


ask "Enter your name" and store in username;
ask "Enter your age" and store in age;


### Examples

print greeting = "Hello World";
set sum = 5 + 3;
print total = sum;
ask "What is your favorite color?" and store in color;


---

## 4. 🧮 Operators

### ➕➖ Arithmetic Operators
- `+` : Addition
- `-` : Subtraction
- `*` : Multiplication
- `/` : Division

### 🔗 Comparison Operators
- `==` : Equality
- `!=` : Not equal
- `>`  : Greater than
- `<`  : Less than
- `>=` : Greater or equal
- `<=` : Less or equal

### 🧠 Logical Operators
- `and` : Logical AND
- `or` : Logical OR
- `not` : Logical NOT

### Examples

set sum = 5 + 3; // 8
set difference = 10 - 3; // 7
set product = 4 * 5; // 20
set quotient = 20 / 4; // 5

if age > 18 {
print status = "Adult";
}


---

## 5. Conditional Statements (If/Else)

### Syntax

if (condition) {
statements;
} else {
statements;
}


### Features
- `else` block is optional
- Nested if statements are supported

### Examples

if (age > 18) {
print status = "Adult";
} else {
print status = "Minor";
}

if (grade == "A" and score > 90) {
print result = "Excellent";
}


---

## 6. Loops

### While Loop

while (condition) {
statements;
}


### Count Loop (For)

for set i = 0; i < 5; i = i + 1 {
statements;
}


### For Each Loop

for each item in list_name {
statements;
}


### Examples

// While Loop
set counter = 1;
while (counter < 10) {
print c = counter;
set counter = counter + 1;
}

// Count Loop
for set i = 0; i < 5; i = i + 1 {
print i = i;
}

// For Each Loop
set fruits = "apple","banana","orange";
for each fruit in fruits {
print f = fruit;
}

```
---

## 7. Functions

### Define a Function

func function_name(param1, param2) {
statements;
return expression;
}


### Call a Function

set result = call function_name(arg1, arg2);


### Return Statement
Functions can return values using `return`:


return expression;


### Examples

func add_numbers(x, y) {
set result = x + y;
return result;
}

set sum = call add_numbers(5, 3);
print total = sum;

func greet(name) {
print msg = "Hello " + name;
}

call greet("John");


---

## 8. Comments
Comments start with `//` and continue to the end of the line:


// This is a comment
set age = 25; // This variable stores the age


---

## 9. Variable Scope
- Variables are **global** by default
- **Function parameters** create local scope
- Local variables shadow global variables within their function
- Function scope is cleaned up after the function returns

---

## 10. Truthy/Falsy Values
In conditional contexts, values are evaluated as:
- **Truthy**: Non-zero numbers, non-empty strings/lists, `true`
- **Falsy**: Zero, empty string/list, `false`

---

## 11. Type Coercion
- Numbers can be added to strings (concatenation)
- Implicit conversion happens in arithmetic operations
- Input from `ask` tries to parse as number first, then string

---

## 12. Complete Language Grammar (BNF)

```
program : class_def*
class_def : CLASS IDENTIFIER LBRACE func_def* RBRACE
func_def : FUNC IDENTIFIER LPAREN param_list? RPAREN LBRACE statement* RBRACE
param_list : IDENTIFIER (COMMA IDENTIFIER)*
statement : set_stmt | print_stmt | if_stmt | while_stmt | for_stmt | func_call | return_stmt
set_stmt : SET IDENTIFIER EQUAL expression SEMICOLON
print_stmt : PRINT IDENTIFIER EQUAL expression SEMICOLON
if_stmt : IF LPAREN expression RPAREN LBRACE statement* RBRACE (ELSE LBRACE statement* RBRACE)?
while_stmt : WHILE LPAREN expression RPAREN LBRACE statement* RBRACE
for_stmt : FOR IDENTIFIER EQUAL expression SEMICOLON expression SEMICOLON expression LBRACE statement* RBRACE
for_each_stmt : FOR EACH IDENTIFIER IN expression LBRACE statement* RBRACE
func_call : CALL IDENTIFIER LPAREN arg_list? RPAREN SEMICOLON
return_stmt : RETURN expression SEMICOLON
expression : addition ((PLUS | MINUS) addition)*
addition : multiplication ((TIMES | DIVIDE) multiplication)*
multiplication : unary
unary : NOT unary | primary
primary : NUMBER | STRING | BOOLEAN | IDENTIFIER | func_call
arg_list : expression (COMMA expression)*
```
---

## 13. Limitations
- No file I/O operations
- Only basic lists supported
- No modules or imports
- Limited standard library

---

## 14. Example Programs

### Hello World

print message = "Hello World";


### Variables and Math

set x = 10;
set y = 5;
set sum = x + y;
print total = sum;


### Conditional Logic

set age = 20;
if (age > 18) {
print status = "Adult";
} else {
print status = "Minor";
}


### Loops

set i = 1;
while (i < 6) {
print n = i;
set i = i + 1;
}


### Functions

func multiply(a, b) {
return a * b;
}
set result = call multiply(3, 4);
print product = result;


### Full Class Example

class ProjectExample {
func main() {
print greeting = "Hello World";
set a = 10;
set b = 5;
print sum = a + b;
print difference = a - b;
print product = a * b;
print quotient = a / b;

    if (a > b) {
        print bigger = "a is bigger";
    } else {
        print bigger = "b is bigger";
    }

    set i = 0;
    while (i < 3) {
        print count = i;
        set i = i + 1;
    }
}

}
