# Nallix Operating System

Nallix is a lightweight, Python-based operating system featuring a terminal interface, built-in development tools, file management, and a text editor. It provides a complete computing environment with process management, user sessions, and system utilities.

## Features

- **Operating System Core**
  - Process management and execution
  - File system with hierarchical directory structure
  - User account management and authentication
  - Persistent sessions and system state
  - Custom shell with command history
  - System resource management

- **Integrated Development Tools**
  - Nalvim: Lightweight text editor with vim-like keybindings
  - Assemplex: Stack-based programming language with VM
  - File management utilities
  - Process execution

- **System Commands**
  - File operations: ls, cd, mkdir, rmdir, copy, move, del
  - Text processing: type, echo
  - System: cls, help, exit
  - User management: create user, change user

## Getting Started

### Prerequisites
- Python 3.7 or later
- Windows (primary platform, may work on other OS with modifications)
- 10MB free disk space
- 512MB RAM (minimum)

### Installation
1. Clone the repository
2. Navigate to the Nallix directory
3. Run `python Terminal.py`

## Available Commands

### File Operations
- `ls` - List directory contents
- `cd [dir]` - Change directory
- `pwd` - Print working directory
- `mkdir [name]` - Create directory
- `rmdir [name]` - Remove directory
- `touch [file]` - Create empty file
- `del [file]` - Delete file
- `copy [src] [dst]` - Copy file
- `move [src] [dst]` - Move/rename file

### Text Editing
- `nalvim [file]` or `nv [file]` - Open Nalvim editor
- `type [file]` - Display file contents

### Programming
- `assemplex [file]` or `asp [file]` - Run Assemplex code

### User Management
- `create user` - Create new user
- `change user` - Switch user
- `log out` - Sign out current user

## Documentation

- [Assemplex Language Reference](ASSEMPLEX_README.md)
- [Nalvim Editor Guide](NALVIM_README.md)

## Customization

### Environment Variables
- `NALLIX_HOME` - Base directory for Nallix (default: current directory)
- `NALLIX_USER` - Default username (default: guest)

## Development

### System Architecture

```
Nallix/
├── bin/                # Core system binaries
│   ├── Terminal.py     # Main system shell
│   ├── Assemplex.py    # Assemplex language implementation
│   └── nalvim.py       # Text editor
│
├── Home/              # User home directories
│   ├── Lasking/       # User directories
│   └── [username]/    # Other user directories
```

### Building from Source
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the terminal:
   ```bash
   python bin/Terminal.py
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by Unix shells and Vim
- Built with Python's standard library
