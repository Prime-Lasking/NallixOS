# Assemplex Programming Language

Assemplex is a stack-based programming language with a virtual machine, designed for the Nallix environment. It features an interactive REPL and supports file execution, making it ideal for learning and scripting.

## Features

- **Stack-Based Architecture**
  - Simple, intuitive operation model
  - Easy-to-learn instruction set
  - Efficient execution

- **Development Tools**
  - Interactive REPL for testing
  - File execution support
  - Debugging capabilities

- **Core Operations**
  - Arithmetic and logical operations
  - Stack manipulation
  - Control flow
  - I/O operations

## Getting Started

### Running the REPL
```bash
# Start interactive mode
assemplex
# or use the shorthand:
asp
```

### Running a Script
```bash
# Execute a script file
assemplex script.ax
# or use the shorthand:
asp script.ax
```

## Language Reference

### Stack Operations
- `PUSH n`: Push value n onto the stack
- `POP`: Remove the top value from the stack
- `DUP`: Duplicate the top stack value
- `SWAP`: Swap the top two stack values

### Arithmetic Operations
- `ADD`: Add top two values
- `SUB`: Subtract top value from second value
- `MUL`: Multiply top two values
- `DIV`: Divide second value by top value
- `MOD`: Modulo operation

### I/O Operations
- `PRINT`: Print top of stack
- `READ`: Read input from user

### Control Flow
- `JMP addr`: Jump to address
- `JZ addr`: Jump if zero
- `JNZ addr`: Jump if not zero
- `HALT`: Stop execution

## Example Program
```
# Simple program to add two numbers
PUSH 5
PUSH 7
ADD
PRINT
HALT
```

## Error Codes
- `0`: Success
- `1`: Division by zero
- `2`: Modulo by zero
- `3`: Stack underflow
- `4`: Bad return address
- `5`: Unknown function
- `6`: Runtime error
