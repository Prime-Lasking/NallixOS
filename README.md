# Nallix Operating System

Nallix is a lightweight, Python-based operating system featuring both terminal and desktop interfaces, built-in development tools, file management, and a text editor. It provides a complete computing environment with process management, user sessions, and system utilities.

## Features

- **Operating System Core**
  - Process management and execution
  - File system with hierarchical directory structure
  - User account management and authentication
  - Persistent sessions and system state
  - Custom shell with command history
  - System resource management

- **Desktop Environment**
  - Modern, customizable desktop interface
  - Right-click on desktop to access context menu
  - Double-click files/folders to open them
  - Create new files/folders from the context menu
  - Change wallpaper through the context menu
  - Access terminal and file explorer from desktop icons or start menu with quick access to applications
  - Right-click context menu for desktop actions
  - File and folder management through GUI
  - Wallpaper customization
  - System tray with clock
  - Start menu with quick access to applications

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

### System Requirements
- Python 3.7 or later
- Windows (primary platform, may work on other OS with modifications)
- 10MB free disk space
- 1GB RAM (minimum, 2GB recommended for desktop mode)
- 1024x768 display resolution (for desktop mode)

### Installation
1. Clone the repository
2. Navigate to the Nallix directory
3. Run either:
   - Terminal mode: `python Terminal.py`
   - Desktop mode: `python bin/desktop.py` or use the `kex` command from the terminal

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
- Right-click desktop → Log Out - Sign out from desktop

## Documentation

- [Assemplex Language Reference](./bin/ASSEMPLEX_README.md)
- [Nalvim Editor Guide](./bin/NALVIM_README.md)

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
│   ├── desktop.py      # Desktop environment
│   ├── Assemplex.py    # Assemplex language implementation
│   └── nalvim.py       # Text editor
│
├── Home/              # User home directories
│   ├── Guest/         # Guest user directories
│   └── [username]/    # Other user directories
│       └── home/      # User's home directory (desktop files)
```

### Building from Source
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run in terminal mode:
   ```bash
   python bin/Terminal.py
   ```
   Or in desktop mode:
   ```bash
   python bin/desktop.py
   ```
   Or from the terminal, use the `kex` command to launch the desktop in a new window.
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
