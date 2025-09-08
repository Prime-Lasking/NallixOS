# Nallix Operating System

Nallix is a lightweight, Python-based operating system featuring both terminal and desktop interfaces, built-in development tools, file management, and a text editor. It provides a complete computing environment with process management, user sessions, and system utilities.

## 🚀 Key Features

### 🖥️ Operating System Core
- **Process Management**
  - Multi-process execution with priority scheduling
  - Process isolation and resource allocation
  - Background process support

- **File System**
  - Hierarchical directory structure
  - File permissions and ownership
  - Symbolic links support
  - Disk usage monitoring

- **User Management**
  - Multi-user support with authentication
  - Role-based access control
  - Password hashing for security
  - Session management

- **Terminal & Shell**
  - Custom shell with command history
  - Command auto-completion
  - Pipes and redirection
  - Environment variables
  - Scripting support

### 🖥️ Desktop Environment
- **User Interface**
  - Modern, themeable interface
  - Customizable desktop layout
  - Multiple virtual desktops
  - Window management (minimize, maximize, close)
  - Drag and drop support

- **File Management**
  - Graphical file explorer
  - File operations (copy, move, delete, rename)
  - File search functionality
  - Thumbnail previews
  - Archive handling

- **Customization**
  - Multiple themes support (light/dark/high contrast)
  - Custom wallpapers
  - Icon sets
  - Font and display settings

- **System Tools**
  - System monitor
  - Task manager
  - Network configuration
  - Display settings
  - Power management

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
│   ├── Lasking/       # User directories
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
