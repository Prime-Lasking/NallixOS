# Assemplex Virtual Machine

Assemplex is a simple, stack-based virtual machine designed for educational purposes and embedded within Nallix OS. It provides a minimal but powerful instruction set for writing low-level programs.

## Table of Contents
- [Quick Start](#quick-start)
- [Instruction Set](#instruction-set)
- [Data Types](#data-types)
- [Memory Model](#memory-model)
- [Error Handling](#error-handling)
- [Examples](#examples)
- [Best Practices](#best-practices)

## Quick Start

1. Create a new file with `.asp` extension:
   ```bash
   nalim program.asp
   ```

2. Write your program:
   ```asm
   ; Simple program to add two numbers
   PUSH 10     ; Push 10 onto the stack
   PUSH 20     ; Push 20 onto the stack
   ADD         ; Add top two numbers (10 + 20)
   PRINT       ; Print result (30)
   HALT        ; End program
   ```

3. Run the program:
   ```bash
   asp program.asp
   ```

## Instruction Set

### Stack Operations
| Opcode | Operand | Description                        | Stack Before | Stack After |
|--------|---------|------------------------------------|--------------|-------------|
| PUSH   | value   | Push value onto stack              | [...]        | [value, ...]|
| DUP    | -       | Duplicate top stack value          | [a, ...]     | [a, a, ...] |
| SWAP   | -       | Swap top two stack values          | [a, b, ...]  | [b, a, ...] |
| DROP   | -       | Remove top stack value             | [a, b, ...]  | [b, ...]    |

### Arithmetic Operations
| Opcode | Operand | Description                | Stack Before    | Stack After |
|--------|---------|----------------------------|-----------------|-------------|
| ADD    | -       | Add top two values         | [a, b, ...]     | [a+b, ...]  |
| SUB    | -       | Subtract (b - a)           | [a, b, ...]     | [b-a, ...]  |
| MUL    | -       | Multiply                   | [a, b, ...]     | [a*b, ...]  |
| DIV    | -       | Divide (b / a)             | [a, b, ...]     | [b/a, ...]  |
| MOD    | -       | Modulo (b % a)             | [a, b, ...]     | [b%a, ...]  |

### Comparison Operations
| Opcode | Operand | Description                | Stack Before    | Stack After |
|--------|---------|----------------------------|-----------------|-------------|
| EQ     | -       | Equal (a == b)             | [a, b, ...]     | [1/0, ...]  |
| NEQ    | -       | Not equal (a != b)         | [a, b, ...]     | [1/0, ...]  |
| GT     | -       | Greater than (b > a)       | [a, b, ...]     | [1/0, ...]  |
| LT     | -       | Less than (b < a)          | [a, b, ...]     | [1/0, ...]  |
| GE     | -       | Greater or equal (b >= a)  | [a, b, ...]     | [1/0, ...]  |
| LE     | -       | Less or equal (b <= a)     | [a, b, ...]     | [1/0, ...]  |

### Control Flow
| Opcode | Operand | Description                        |
|--------|---------|------------------------------------|
| JMP    | label   | Jump to label                      |
| JZ     | label   | Jump if top of stack is zero       |
| JNZ    | label   | Jump if top of stack is not zero   |
| CALL   | label   | Call subroutine at label           |
| RET    | -       | Return from subroutine             |
| HALT   | -       | Stop program execution             |

### I/O Operations
| Opcode | Operand | Description                        |
|--------|---------|------------------------------------|
| PRINT  | -       | Print top of stack                 |
| IN     | -       | Read input from user               |

### Variable Operations
| Opcode | Operand | Description                        |
|--------|---------|------------------------------------|
| STORE  | var     | Store top of stack in variable     |
| LOAD   | var     | Push variable value onto stack     |

## Data Types

Assemplex supports the following data types:
- **Integers**: Whole numbers (e.g., `42`, `-7`)
- **Strings**: Enclosed in quotes (e.g., `"Hello"`, `'World'`)
- **Booleans**: `1` (true) or `0` (false)

## Memory Model

- **Stack**: Used for all operations, grows downward
- **Variables**: Stored in a symbol table with automatic memory management
- **Labels**: Used for control flow, must be unique within a program

## Error Handling

Common error codes:
- `EXIT_OK (0)`: Successful execution
- `EXIT_DIVZERO (1)`: Division by zero
- `EXIT_STACKERR (3)`: Stack underflow/overflow
- `EXIT_RUNTIME (6)`: General runtime error

## Examples

### Fibonacci Sequence
```asm
; Calculate first 10 Fibonacci numbers
PUSH 0       ; First number
PUSH 1       ; Second number
PUSH 10      ; Counter

FIB_LOOP:
    DUP       ; Duplicate counter
    JZ DONE   ; If counter is zero, we're done
    
    ; Print current number
    DUP
    PRINT
    
    ; Calculate next number
    SWAP
    DUP
    ADD
    
    ; Decrement counter and loop
    PUSH 1
    SUB
    JMP FIB_LOOP

DONE:
    HALT
```

## Best Practices

1. **Use Comments**: Document your code with `;` comments
2. **Label Clearly**: Use descriptive label names
3. **Stack Management**: Keep track of stack depth
4. **Error Handling**: Check for division by zero and stack underflow
5. **Testing**: Test subroutines independently

For more advanced usage, refer to the source code in `lib/assemplex.py`.
