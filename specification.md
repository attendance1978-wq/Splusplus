# 📖 S++ Language Specification

## 🎯 Overview
S++ (Simplified Programming Plus) is an English-like programming language designed for ease of use and readability. It uses minimal symbols (only commas and periods) and natural English keywords, making it accessible to beginners.

---

## 1. ⌨️ Symbols
Only **two symbols** are allowed in S++:
- **Comma (`,`)**: Separator for lists and function parameters
- **Period (`.`)**: Terminates all statements

---

## 2. 📦 Variables

### 📝 Declaration and Assignment
Variables are created using the `set` keyword:

```
set variable_name to value.
```

### 🎨 Data Types
S++ supports multiple data types:
- **#️⃣ Numbers**: Integers and floats (e.g., `10`, `3.14`)
- **📝 Strings**: Text values (words/sentences)
- **📋 Lists**: Collections of values separated by commas
- **✓ Booleans**: Implicit (truthy/falsy values)

### Examples
```
set age to 25.
set name to john.
set message to hello world.
set numbers to 1, 2, 3, 4, 5.
set total to 0.
```

---

## 3. 📢 Input and Output

### 🖨️ Print/Write
Display values to the console:

```
print expression.
write expression.
```

### ⌨️ Input (Ask)
Get user input:

```
ask what is your name and store in username.
ask enter your age and store in age.
```

### Examples
```
print hello world.
print message.
ask what is your age and store in user_age.
ask enter your favorite color and store in color.
```

---

## 4. 🧮 Operators

### ➕➖ Arithmetic Operators
- `plus`: Addition
- `minus`: Subtraction
- `times`: Multiplication
- `divided by`: Division

### 🔗 Comparison Operators
- `equals`: Equality check
- `is greater than`: Greater than (>)
- `is less than`: Less than (<)

### 🧠 Logical Operators
- `and`: Logical AND
- `or`: Logical OR
- `not`: Logical NOT

### Examples
```
set sum to 5 plus 3.             // 8
set difference to 10 minus 3.    // 7
set product to 4 times 5.        // 20
set quotient to 20 divided by 4. // 5

if age is greater than 18 then
  print you are adult.
end.
```

---

## 5. Conditional Statements (If/Otherwise)

### Syntax
```
if condition then
  statements
otherwise
  statements
end.
```

### Features
- The `otherwise` block is optional
- Conditions can use comparison and logical operators
- Nested if statements are supported

### Examples
```
if age is greater than 18 then
  print you can vote.
otherwise
  print you cannot vote yet.
end.

if grade equals A and score is greater than 90 then
  print excellent.
end.
```

---

## 6. Loops

### While Loop (Repeat While)
Repeat while a condition is true:

```
repeat while condition
  statements
end.
```

### Count Loop (Repeat N Times)
Repeat a specific number of times:

```
repeat count times
  statements
end.
```

### For Each Loop
Iterate through a list:

```
for each item in list_name
  statements
end.
```

### Examples
```
// While Loop
set counter to 1.
repeat while counter is less than 10
  print counter.
  set counter to counter plus 1.
end.

// Count Loop
repeat 5 times
  print hello.
end.

// For Each Loop
set fruits to apple, banana, orange.
for each fruit in fruits
  print fruit.
end.
```

---

## 7. Functions

### Define a Function
```
define function_name with parameter1, parameter2
  statements
  return value.
end.
```

### Call a Function
```
set result to call function_name with argument1, argument2.
```

### Return Statement
Functions can return values using `return`:

```
return expression.
```

### Examples
```
define add_numbers with x, y
  set result to x plus y.
  return result.
end.

set sum to call add_numbers with 5, 3.
print sum.

define greet with name
  print hello, name.
end.

call greet with john.
```

---

## 8. Comments
Comments start with `//` and continue to the end of the line:

```
// This is a comment
set age to 25. // This variable stores the age
```

---

## 9. Variable Scope
- Variables are **global** by default
- **Function parameters** create local scope
- Local variables shadow global variables within their function
- Function scope is cleaned up after the function returns

---

## 10. Truthy/Falsy Values
In conditional contexts, values are evaluated as:
- **Truthy**: Non-zero numbers, non-empty strings, non-empty lists, `true`
- **Falsy**: Zero, empty string, empty list, `false`

---

## 11. Type Coercion
- Numbers can be added to strings (concatenation)
- Implicit conversion happens in arithmetic operations
- Input from `ask` tries to parse as number first, then string

---

## 12. Complete Language Grammar (BNF)

```
program         : statement*
statement       : set_stmt | print_stmt | ask_stmt | if_stmt | repeat_stmt | for_stmt | func_def | func_call | return_stmt
set_stmt        : SET IDENTIFIER TO expression PERIOD
print_stmt      : (PRINT | WRITE) expression PERIOD
ask_stmt        : ASK phrase AND_STORE_IN IDENTIFIER PERIOD
if_stmt         : IF expression THEN statement* (OTHERWISE statement*)? END PERIOD
repeat_stmt     : REPEAT WHILE expression statement* END PERIOD
                | REPEAT expression TIMES statement* END PERIOD
for_stmt        : FOR EACH IDENTIFIER IN expression statement* END PERIOD
func_def        : DEFINE IDENTIFIER (WITH param_list)? statement* END PERIOD
func_call       : CALL IDENTIFIER (WITH arg_list)?
return_stmt     : RETURN expression? PERIOD
expression      : or_expr
or_expr         : and_expr (OR and_expr)*
and_expr        : comparison ((AND | OR) comparison)*
comparison      : addition ((EQUALS | IS_GREATER_THAN | IS_LESS_THAN) addition)*
addition        : multiplication ((PLUS | MINUS) multiplication)*
multiplication  : unary ((TIMES | DIVIDED_BY) unary)*
unary           : (NOT) unary | primary
primary         : NUMBER | IDENTIFIER | CALL
phrase          : (IDENTIFIER | NUMBER)+
param_list      : IDENTIFIER (COMMA IDENTIFIER)*
arg_list        : expression (COMMA expression)*
```

---

## 13. Limitations
- No built-in data structures beyond lists
- No file I/O operations
- No object-oriented features
- No module/import system
- Limited standard library

---

## 14. Example Programs

### Hello World
```
print hello world.
```

### Variables and Math
```
set x to 10.
set y to 5.
set sum to x plus y.
print sum.
```

### Conditional Logic
```
set age to 20.
if age is greater than 18 then
  print you are an adult.
otherwise
  print you are a minor.
end.
```

### Loops
```
set i to 1.
repeat while i is less than 6
  print i.
  set i to i plus 1.
end.
```

### Functions
```
define multiply with a, b
  return a times b.
end.

set result to call multiply with 3, 4.
print result.
```

For more examples, see the `examples/` directory.
