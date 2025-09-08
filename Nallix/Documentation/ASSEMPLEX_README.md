# 🧮 Assemplex Programming Language

Assemplex is a powerful, stack-based programming language with a virtual machine, designed specifically for the Nallix environment. It combines the simplicity of Forth with modern programming concepts, making it ideal for system programming, scripting, and educational purposes.

## ✨ Features

### 🏗️ Stack-Based Architecture
- **Simple Execution Model**
  - Single data stack for all operations
  - Minimalist instruction set
  - Predictable execution flow
  - Efficient memory usage

### 🛠️ Development Tools
- **Interactive REPL**
  - Immediate code execution
  - Syntax highlighting
  - Command history
  - Tab completion

- **Debugging Support**
  - Step-by-step execution
  - Stack inspection
  - Breakpoints
  - Call stack tracing

### ⚡ Core Capabilities
- **Numeric Operations**
  - Integer and floating-point arithmetic
  - Bitwise operations
  - Comparison operators
  - Math functions

- **Control Flow**
  - Conditional branching
  - Loops
  - Subroutine calls
  - Exception handling

- **I/O Operations**
  - Console input/output
  - File handling
  - Network communication
  - Device I/O

## 🚀 Getting Started

### Prerequisites
- Nallix OS installed
- Assemplex package included in your Nallix installation

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

# With command-line arguments
asp script.ax arg1 arg2
```

### Debugging Mode
```bash
# Start in debug mode
asp --debug script.ax

# Set breakpoints
asp --break 10,20,30 script.ax
```

### Example: Hello World
```
# Simple Hello World program
: hello "Hello, World!" ;
hello print
```

### Example: Factorial Function
```
# Recursive factorial
: fact 
    dup 1 > if
        dup 1 - fact * 
    else
        drop 1
    then ;

# Calculate 5!
5 fact .
```

## 📚 Language Reference

### Stack Operations
| Operation | Description | Example | Stack Before | Stack After |
|-----------|-------------|---------|--------------|-------------|
| `PUSH n`  | Push value n onto stack | `5` | `[ ]` | `[ 5 ]` |
| `DUP`     | Duplicate top value | `dup` | `[ 5 ]` | `[ 5 5 ]` |
| `DROP`    | Remove top value | `drop` | `[ 5 5 ]` | `[ 5 ]` |
| `SWAP`    | Swap top two values | `swap` | `[ 5 10 ]` | `[ 10 5 ]` |
| `OVER`    | Copy second value to top | `over` | `[ 5 10 ]` | `[ 5 10 5 ]` |
| `ROT`     | Rotate top three values | `rot` | `[ 1 2 3 ]` | `[ 2 3 1 ]` |

### Arithmetic Operations
| Operation | Description | Example | Stack Before | Stack After |
|-----------|-------------|---------|--------------|-------------|
| `+`       | Add top two values | `+` | `[ 2 3 ]` | `[ 5 ]` |
| `-`       | Subtract top from second | `-` | `[ 5 3 ]` | `[ 2 ]` |
| `*`       | Multiply top two values | `*` | `[ 2 3 ]` | `[ 6 ]` |
| `/`       | Divide second by top | `/` | `[ 6 2 ]` | `[ 3 ]` |
| `MOD`     | Modulo operation | `mod` | `[ 7 3 ]` | `[ 1 ]` |

### Control Flow
| Operation | Description | Example |
|-----------|-------------|---------|
| `IF ... THEN` | Conditional execution | `0 > if ."Positive" then` |
| `BEGIN ... UNTIL` | Loop until condition | `: countdown 10 begin dup . 1- dup 0= until drop ;` |
| `DO ... LOOP` | Counted loop | `: table 11 1 do i . i 5 * . cr loop ;` |

### Memory Operations
| Operation | Description | Example |
|-----------|-------------|---------|
| `!` | Store value at address | `42 0x1000 !` |
| `@` | Fetch value from address | `0x1000 @` |
| `+!` | Add to memory location | `10 0x1000 +!` |
| `C!` | Store byte in memory | `65 0x1000 C!` |
| `C@` | Fetch byte from memory | `0x1000 C@` |

### I/O Operations
| Operation | Description | Example |
|-----------|-------------|---------|
| `.` | Print top of stack | `42 .` |
| `.\"` | Print string | `."Hello"` |
| `KEY` | Read character | `key` |
| `EMIT` | Output character | `65 emit` (prints 'A') |
| `CR` | Print newline | `cr` |

### Defining Words
```
: square ( n -- n^2 )
    dup * ;

: factorial ( n -- n! )
    dup 1 > if
        dup 1 - recurse * 
    else
        drop 1
    then ;
```
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
