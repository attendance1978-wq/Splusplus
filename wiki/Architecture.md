# Architecture

This page explains the interpreter internals and project layout.

High-level components
- Lexer: tokenizes English keywords and symbols (commas, periods)
- Parser: recursive-descent parser building an AST
- Interpreter: visitor-based AST execution with scoped environments

Key files
- `interpreter.py` — single-file implementation (lexer, parser, AST, interpreter)
- `specification.md` — full language grammar and rules
- `examples/` — sample programs used for testing and demonstration

Design notes
- Multi-word operators are normalized during lexing (e.g., "divided by")
- Identifiers can fall back to string literals in print/assignment contexts
- No native or filesystem access; intended for educational use

Extending the interpreter
- Add AST nodes in parser and handle in interpreter visitor
- Keep changes minimal and add unit tests under a `tests/` folder
