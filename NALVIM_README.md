# Nalvim Text Editor

Nalvim is a simple, lightweight text editor integrated into the Nallix terminal environment. It provides basic text editing capabilities with a vim-like interface.

## Features

- Modal editing (Normal/Insert modes)
- Basic file operations
- Simple navigation
- Line operations
- Syntax highlighting (basic)
- Persistent cursor position

## Getting Started

### Launching Nalvim
```bash
nalvim [filename]
# or use the shorthand:
nv [filename]
```

If no filename is provided, Nalvim will start with an empty buffer.

## Modes

### Normal Mode (Default)
This is the default mode when you start Nalvim. Use it for navigation and commands.

### Insert Mode
Enter text input mode. Press `ESC` to return to Normal mode.

## Basic Commands

### Navigation (Normal Mode)
- `h` - Move cursor left
- `j` - Move cursor down
- `k` - Move cursor up
- `l` - Move cursor right
- `0` - Move to start of line
- `$` - Move to end of line
- `gg` - Move to first line
- `G` - Move to last line
- `:n` - Jump to line n (e.g., `:10` goes to line 10)

### Editing
- `i` - Enter insert mode at cursor
- `a` - Enter insert mode after cursor
- `x` - Delete character under cursor
- `dd` - Delete current line
- `u` - Undo
- `Ctrl+r` - Redo

### File Operations
- `:w` - Save file
- `:w filename` - Save as new file
- `:wq` - Save and quit
- `:q` - Quit (if no changes)
- `:q!` - Force quit (discard changes)
- `:e filename` - Open another file

### Search
- `/pattern` - Search forward for pattern
- `?pattern` - Search backward for pattern
- `n` - Next match
- `N` - Previous match

## Configuration

Nalvim automatically saves your cursor position and restores it when you reopen files. This behavior can be customized by modifying the `~/.nalvimrc` file (if available).

## Known Limitations

- No visual selection
- Limited undo/redo history
- Basic syntax highlighting only
- No split windows or tabs

## Tips

- Use `:help` in Nalvim for quick reference
- Press `ESC` twice to ensure you're in Normal mode
- Combine commands with numbers (e.g., `3dd` deletes 3 lines)
- Use `:w` frequently to save your work
