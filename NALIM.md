# Nalim Text Editor

Nalim is a lightweight, vim-inspired text editor integrated into Nallix OS. It provides a modal editing experience with familiar keybindings for efficient text manipulation.

## Table of Contents
- [Getting Started](#getting-started)
- [Modes](#modes)
- [Navigation](#navigation)
- [Editing](#editing)
- [Saving and Quitting](#saving-and-quitting)
- [Advanced Features](#advanced-features)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Getting Started

### Launching Nalim
```bash
nalim filename.txt       # Open or create a file
nalim /path/to/file.txt  # Open with full path
```

### Basic Workflow
1. Open a file with `nalim filename`
2. Use normal mode for navigation and commands
3. Press `i` to enter insert mode for text entry
4. Press `ESC` to return to normal mode
5. Save with `:w` and quit with `:q`

## Modes

### 1. Normal Mode (Default)
- For navigation and commands
- Press `ESC` to return from other modes
- Shows `NORMAL` in status bar

### 2. Insert Mode
- For text entry
- Enter with `i` from normal mode
- Shows `INSERT` in status bar
- Press `ESC` to return to normal mode

### 3. Command Mode
- For file operations and quitting
- Enter with `:` from normal mode
- Shows `:` prompt at bottom
- Press `ESC` or `Enter` to cancel

## Navigation

### Basic Movement (Normal Mode)
| Key | Action                      |
|-----|-----------------------------|
| `w` | Move up                     |
| `s` | Move down                   |
| `a` | Move left                   |
| `d` | Move right                  |
| `0` | Start of line               |
| `$` | End of line                 |
| `gg`| First line of file          |
| `G` | Last line of file           |
| `:n`| Go to line n (e.g., `:10`)   |

### Scrolling
| Key   | Action                      |
|-------|-----------------------------|
| `Ctrl+u` | Scroll up half page        |
| `Ctrl+d` | Scroll down half page      |
| `Ctrl+b` | Scroll up one page         |
| `Ctrl+f` | Scroll down one page       |

## Editing

### Inserting Text
| Command | Action                      |
|---------|-----------------------------|
| `i`     | Insert before cursor        |
| `a`     | Insert after cursor         |
| `o`     | Insert new line below       |
| `O`     | Insert new line above       |

### Deleting Text
| Command | Action                      |
|---------|-----------------------------|
| `x`     | Delete character at cursor  |
| `dd`    | Delete current line         |
| `dw`    | Delete word                 |
| `D`     | Delete to end of line       |

### Copy and Paste
| Command | Action                      |
|---------|-----------------------------|
| `yy`    | Yank (copy) current line    |
| `p`     | Paste after cursor          |
| `P`     | Paste before cursor         |

## Saving and Quitting

### Basic Commands
| Command | Action                      |
|---------|-----------------------------|
| `:w`    | Save file                   |
| `:q`    | Quit (fails if unsaved)     |
| `:q!`   | Quit without saving         |
| `:wq`   | Save and quit               |
| `:x`    | Save and quit (same as `:wq`)|

### File Operations
| Command | Action                      |
|---------|-----------------------------|
| `:e filename` | Edit another file    |
| `:w filename` | Save as new file     |
| `:r filename` | Insert file contents |

## Advanced Features

### Search and Replace
| Command | Action                      |
|---------|-----------------------------|
| `/text` | Search forward for 'text'   |
| `?text` | Search backward for 'text'  |
| `n`     | Next match                 |
| `N`     | Previous match             |
| `:%s/old/new/g` | Replace all 'old' with 'new' |

### Multiple Windows
| Command | Action                      |
|---------|-----------------------------|
| `:sp`   | Split window horizontally   |
| `:vsp`  | Split window vertically     |
| `Ctrl+w w` | Switch between windows    |
| `Ctrl+w q` | Close current window     |

## Configuration

Nalim can be configured by creating a `.nalimrc` file in your home directory. Example:

```ini
# Enable line numbers
set number

# Set tab width to 4 spaces
set tabstop=4
set shiftwidth=4
set expandtab

# Enable syntax highlighting
syntax on

# Set color scheme
colorscheme desert
```

## Troubleshooting

### Common Issues
1. **Stuck in Insert Mode**
   - Press `ESC` multiple times
   - Try `Ctrl+[` as an alternative

2. **Unresponsive Editor**
   - Check for pending commands (look for `:` prompt)
   - Try pressing `ESC` then `:` to enter command mode

3. **Can't Save File**
   - Check file permissions
   - Try `:w!` to force write (if permissions allow)
   - Use `:w newname` to save with a different name

### Getting Help
- `:help` - Show help
- `:version` - Show version information
- `:commands` - List all available commands

## Tips and Tricks
- Press `.` to repeat last edit
- Use `u` to undo and `Ctrl+r` to redo
- Combine commands with counts (e.g., `3dd` deletes 3 lines)
- Use `v` for visual mode to select text
- `:!command` runs a shell command (e.g., `:!ls`)

For feature requests or bug reports, please open an issue in the Nallix OS repository.
