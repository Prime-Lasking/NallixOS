# Nallix Terminal Environment

Nallix is a lightweight, extensible terminal environment with built-in tools and programming languages. It provides a unified interface for file management, text editing, and programming.

## Features

- **Integrated Development Environment**
  - Built-in text editor (Nalvim)
  - Assemplex programming language
  - File system navigation
  - User management

- **Key Components**
  - Terminal shell with command history
  - Persistent user sessions
  - Extensible command system
  - Cross-platform compatibility

## Getting Started

### Prerequisites
- Python 3.7+
- Windows (for full functionality)

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

- [Assemplex Language Reference](./bin/ASSEMPLEX_README.md)
- [Nalvim Editor Guide](./bin/NALVIM_README.md)

## Customization

### Configuration Files
- `~/.nallixrc` - User configuration (not implemented yet)
- `~/.nalvimrc` - Nalvim configuration (not implemented yet)

### Environment Variables
- `NALLIX_HOME` - Base directory for Nallix (default: current directory)
- `NALLIX_USER` - Default username (default: guest)

## Development

### Project Structure
```
Nallix/
├── bin/                 # Core binaries
│   ├── Terminal.py      # Main terminal
│   ├── Assemplex.py     # Assemplex language
│   └── nalvim.py        # Text editor
├── Home/               # User home directories
└── README.md           # This file
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
