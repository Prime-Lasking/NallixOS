# Nallix OS

A lightweight operating system built in Python with a command-line interface, featuring a text editor and Assemplex VM integration.

## Table of Contents
- [Getting Started](#getting-started)
- [Basic Commands](#basic-commands)
- [Nalim Text Editor](#nalim-text-editor)
- [Assemplex VM](#assemplex-vm)
- [File System](#file-system)
- [User Management](#user-management)
- [Process Management](#process-management)
- [License](#license)

## Getting Started

1. Run the main script:
   ```bash
   python Nallix/Main.py
   ```

2. Log in with an existing user or create a new one.

## Basic Commands

| Command   | Description                          | Example                   |
|-----------|--------------------------------------|---------------------------|
| `ls`      | List directory contents              | `ls`                      |
| `cd`      | Change directory                     | `cd documents`            |
| `mkdir`   | Create a directory                   | `mkdir new_folder`        |
| `touch`   | Create a file                        | `touch file.txt`          |
| `cat`     | Display file contents                | `cat file.txt`            |
| `pwd`     | Print working directory              | `pwd`                     |
| `echo`    | Print text                           | `echo "Hello, World!"`    |
| `rm`      | Remove a file or directory           | `rm file.txt`             |
| `whoami`  | Show current user                    | `whoami`                  |
| `nallix`  | Show system information              | `nallix`                  |
| `help`    | Show help for commands               | `help` or `help command`  |

## Nalim Text Editor

Nalim is a simple, vim-like text editor with the following features:

### Opening Files
```bash
nalim filename.txt
# or
vedit filename.txt  # vedit is an alias for nalim
```

### Navigation (Normal Mode)
- `w` - Move up
- `s` - Move down
- `a` - Move left
- `d` - Move right
- `i` - Enter insert mode
- `ESC` - Return to normal mode

### Commands (Normal Mode)
- `:w` - Save file
- `:q` - Quit without saving
- `:wq` - Save and quit

## Assemplex VM

Assemplex is a simple stack-based virtual machine for running `.asp` files.

### Running Programs
```bash
asp program.asp
# or
asp program  # .asp extension is optional
```

### Example Program
```asm
; Simple addition program
PUSH 10
PUSH 20
ADD
PRINT  ; Prints 30
HALT
```

### Available Opcodes
- Stack: `PUSH`, `POP`, `DUP`, `SWAP`, `DROP`
- Arithmetic: `ADD`, `SUB`, `MUL`, `DIV`, `MOD`
- Comparison: `EQ`, `NEQ`, `GT`, `LT`, `GE`, `LE`
- Logic: `AND`, `OR`, `NOT`
- Control Flow: `JMP`, `JZ`, `JNZ`, `CALL`, `RET`
- I/O: `PRINT`, `IN`
- Variables: `STORE`, `LOAD`
- System: `HALT`, `DEBUG`

## File System

Nallix OS provides a sandboxed file system with the following features:
- User home directories
- File permissions
- Basic file operations

## User Management

- `create` - Create a new user
- `change` - Switch users
- `current` - Show current user
- `logout` - Log out current user

## Process Management

| Command | Description                    | Example        |
|---------|--------------------------------|----------------|
| `ps`    | List running processes         | `ps`           |
| `kill`  | Terminate a process by PID     | `kill 1234`    |

## License

This project is open source and available under the MIT License.

---

For more information or to contribute, please visit the project repository.
