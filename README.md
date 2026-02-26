<p align="center">
  <img src="icon/S++.png" width="400" alt="S++ Programming Language Icon">
</p>

<h1 align="center">📚 S++ Programming Language</h1>

<p align="center">
  ✨ An English-like programming language interpreter built in Python.<br>
  Write software using simple English sentences, commas, and periods.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python-blue">
  <img src="https://img.shields.io/badge/Type-Interpreter-green">
  <img src="https://img.shields.io/badge/Syntax-English-orange">
  <img src="https://img.shields.io/badge/Status-Development-yellow">
  <img src="https://www.freewebtools.com/api/badge/Splusplus-EDUCATIONAL%20PURPOSE%20ONLY-4c1.svg?style=rounded&labelColor=1000">
</p>
## ✨ Features

🔤 **Simple English Syntax** - No complex symbols, just English keywords  
⚙️ **Minimal Symbols** - Only commas and periods allowed  
🎯 **Core Programming Concepts** - Variables, conditionals, loops, functions  
💬 **Easy Input/Output** - User-friendly `ask` and `print` statements  
⚡ **Functional Programming** - First-class functions with parameters and returns  

## 📦 Installation

### 📋 Requirements
- Python 3.7 or higher

### 🔧 Setup
1. Clone or download the repository
2. No external dependencies needed - uses only Python standard library

## Quick Start

### Run a Program File
```bash
python interpreter.py program.spp
```

### Interactive Mode
```bash
python interpreter.py
```
Enter your code line by line and type `STOP.` on a new line to execute.

## 📖 Language Basics

### 🖨️ Print to Console
```
print hello world.
```

### 📝 Create Variables
```
set age to 25.
set name to john.
```

### ⌨️ Get User Input
```
ask what is your name and store in username.
```

### 🔀 Conditional Logic
```
if age is greater than 18 then
  print you are an adult.
otherwise
  print you are a minor.
end.
```

### 🔁 Loops
```
repeat 5 times
  print hello.
end.

repeat while counter is less than 10
  print counter.
  set counter to counter plus 1.
end.
```

### ⚙️ Functions
```
define add with x, y
  return x plus y.
end.

set result to call add with 3, 5.
print result.
```

## Examples

The `examples/` directory contains 10 complete programs demonstrating all features:

| File | Description |
|------|-------------|
| `01_hello_world.spp` | Basic hello world |
| `02_variables.spp` | 📝 Variable declaration and types |
| `03_arithmetic.spp` | ➕ Math operations |
| `04_conditionals.spp` | 🔀 If/otherwise statements |
| `05_loops.spp` | 🔁 While and repeat loops |
| `06_functions.spp` | ⚙️ Function definition and calls |
| `07_lists.spp` | 📋 List processing with for each |
| `08_calculator.spp` | 🧮 Interactive calculator (complex) |
| `09_factorial.spp` | 🔢 Factorial calculation |
| `10_grades.spp` | 📊 Grade calculator with feedback |

### Run Examples
```bash
python interpreter.py examples/01_hello_world.spp
python interpreter.py examples/06_functions.spp
python interpreter.py examples/08_calculator.spp
```

## Language Documentation

See [specification.md](specification.md) for complete language documentation including:
- All keywords and operators
- Grammar and syntax rules
- Data types and type coercion
- Variable scoping
- Complete language reference

## Language Syntax Overview

### Keywords
- **Variables**: `set`, `to`
- **I/O**: `print`, `write`, `ask`, `and store in`
- **Control Flow**: `if`, `then`, `otherwise`, `end`, `repeat`, `while`, `times`, `for`, `each`, `in`
- **Functions**: `define`, `with`, `call`, `return`

### Operators
- **Arithmetic**: `plus`, `minus`, `times`, `divided by`
- **Comparison**: `equals`, `is greater than`, `is less than`
- **Logical**: `and`, `or`, `not`

### Symbols
- **Comma (`,`)**: Separates list items and function parameters
- **Period (`.`)**: Terminates every statement

## Program Structure

Every S++ program consists of:
1. **Function definitions** (optional)
2. **Variable declarations** (optional)
3. **Executable statements** (required)
4. Every statement ends with a period

```
define greet with name
  print hello, name.
end.

set username to alice.
call greet with username.
```

## Interpreter Architecture

### Lexer
Tokenizes the input text, recognizing keywords, identifiers, numbers, and symbols.

### Parser
Builds an Abstract Syntax Tree (AST) from tokens using recursive descent parsing.

### Interpreter
Walks the AST and executes the program, maintaining:
- Global variable scope
- Function definitions
- Execution state

## Error Handling

The interpreter provides error messages for:
- Unexpected tokens and parsing errors
- Undefined variables or functions
- Type errors in operations
- Division by zero

## Limitations

- No file I/O operations
- No standard library functions (math, string manipulation, etc.)
- No object-oriented features
- No module/import system
- Limited operator overloading

## Future Enhancements

Potential features for future versions:
- String manipulation functions
- More complex data structures (dictionaries, tuples)
- Exception handling (try/catch)
- File I/O operations
- Debugging mode with breakpoints
- Optimization and compilation

## License

This project is open source and available for educational purposes.

## Author

Built as a demonstration of language design and interpreter implementation.

---

**Happy Coding in S++!** 🚀


