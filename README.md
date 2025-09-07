# Nallix Operating System

Nallix is a lightweight, operating system with a built-in terminal environment. It provides core OS functionality along with development tools, file management, and a text editor, all within a Python-based environment.

## Features

- **Core Operating System**
  - Process management
  - File system operations
  - User management and permissions
  - Terminal interface

- **Development Tools**
  - Nalvim text editor
  - Assemplex programming language and VM
  - File system navigation and management
  - Scripting capabilities

- **System Components**
  - Terminal shell with command history
  - Persistent user sessions
  - Extensible command system
  - Cross-platform compatibility layer

## Getting Started

### Prerequisites
- Python 3.7+ (temporary runtime environment)
- Windows (primary development platform)
- 100MB free disk space (minimum)
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
## Customization

### Environment Variables
- `NALLIX_HOME` - Base directory for Nallix (default: current directory)
- `NALLIX_USER` - Default username (default: guest)

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
