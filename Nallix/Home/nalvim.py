import sys
import os
import msvcrt
from typing import List

def get_key():
    """Get a single keypress with comprehensive error handling"""
    try:
        if os.name == 'nt':  # Windows
            ch = msvcrt.getch()
            # Handle special keys (arrows, function keys, etc.)
            if ch in (b'\x00', b'\xe0'):
                ch2 = msvcrt.getch()  # Get the next byte
                # Map arrow keys to wasd for movement
                if ch2 == b'H':  # Up
                    return 'w'
                elif ch2 == b'P':  # Down
                    return 's'
                elif ch2 == b'K':  # Left
                    return 'a'
                elif ch2 == b'M':  # Right
                    return 'd'
                return ''  # Ignore other special keys
            
            # Handle backspace and delete
            if ch == b'\x08' or ch == b'\x7f':
                return '\x7f'  # Standardize backspace
                
            # Handle escape key
            if ch == b'\x1b':
                return '\x1b'
                
            # Handle enter/return
            if ch == b'\r' or ch == b'\n':
                return '\r'
                
            # Try to decode as UTF-8
            try:
                return ch.decode('utf-8')
            except UnicodeDecodeError:
                return ''  # Skip unhandled special keys
                
        else:  # Unix/Linux
            import tty, termios, fcntl
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                # Handle escape sequences for arrow keys
                if ch == '\x1b':
                    ch = sys.stdin.read(1)
                    if ch == '[':
                        ch = sys.stdin.read(1)
                        if ch == 'A': return 'w'  # Up
                        if ch == 'B': return 's'  # Down
                        if ch == 'D': return 'a'  # Left
                        if ch == 'C': return 'd'  # Right
                return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                
    except Exception as e:
        print(f"\nError in get_key: {e}")
        return ''

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_buffer(buffer: List[str], cursor_x: int, cursor_y: int, mode: str, command_mode=False, command=""):
    """Display the buffer with cursor and mode indicator"""
    clear_screen()
    for i, line in enumerate(buffer):
        if i == cursor_y:
            # Insert cursor
            print(line[:cursor_x] + '|' + line[cursor_x:])
        else:
            print(line)
    
    # Status line
    status = f"-- {mode.upper()} --"
    if command_mode:
        status = f":{command}"
    print(f"\n{status}")
    if not command_mode:
        print("WASD: Move | i: Insert | x: Delete char | dd: Delete line | :q: Quit")

def main():
    # Initialize buffer with command line argument if provided
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        with open(sys.argv[1], 'r') as f:
            buffer = [line.rstrip('\n') for line in f]
    else:
        buffer = [""]
    
    cursor_x = 0
    cursor_y = 0
    mode = "normal"
    command_mode = False
    command = ""
    last_key = ''

    while True:
        display_buffer(buffer, cursor_x, cursor_y, mode, command_mode, command)
        
        if command_mode:
            print(f":{command}", end="", flush=True)
            
        key = get_key()
        
        if command_mode:
            if key == '\r':  # Enter
                if command == 'q':
                    return
                command_mode = False
                command = ""
                continue
            elif key == '\x7f':  # Backspace
                command = command[:-1]
            else:
                command += key
            continue
                
        if mode == "normal":
            if key == ':':
                command_mode = True
                command = ""
                continue
                
            # Movement
            if key == 'w' and cursor_y > 0:
                cursor_y -= 1
                cursor_x = min(cursor_x, len(buffer[cursor_y]))
            elif key == 's' and cursor_y < len(buffer) - 1:
                cursor_y += 1
                cursor_x = min(cursor_x, len(buffer[cursor_y]))
            elif key == 'a' and cursor_x > 0:
                cursor_x -= 1
            elif key == 'd' and cursor_x < len(buffer[cursor_y]):
                cursor_x += 1
            # Commands
            elif key == 'i':
                mode = "insert"
            elif key == 'x' and cursor_x < len(buffer[cursor_y]):
                buffer[cursor_y] = buffer[cursor_y][:cursor_x] + buffer[cursor_y][cursor_x + 1:]
            elif key == 'd':
                if last_key == 'd':  # dd - delete line
                    if len(buffer) > 1:
                        buffer.pop(cursor_y)
                        cursor_y = min(cursor_y, len(buffer) - 1)
                        cursor_x = min(cursor_x, len(buffer[cursor_y]))
            last_key = key

        elif mode == "insert":
            if key == '\x1b':  # ESC key
                mode = "normal"
            elif key == '\r':  # Enter key
                # Split current line at cursor
                new_line = buffer[cursor_y][cursor_x:]
                buffer[cursor_y] = buffer[cursor_y][:cursor_x]
                buffer.insert(cursor_y + 1, new_line)
                cursor_y += 1
                cursor_x = 0
            elif key == '\x7f':  # Backspace
                if cursor_x > 0:
                    buffer[cursor_y] = buffer[cursor_y][:cursor_x-1] + buffer[cursor_y][cursor_x:]
                    cursor_x -= 1
                elif cursor_y > 0:
                    cursor_x = len(buffer[cursor_y - 1])
                    buffer[cursor_y - 1] += buffer[cursor_y]
                    buffer.pop(cursor_y)
                    cursor_y -= 1
            else:
                # Handle all other keys
                if key:  # Only process if we got a valid key
                    if len(key) == 1 and ord(key) >= 32:  # Printable characters
                        buffer[cursor_y] = buffer[cursor_y][:cursor_x] + key + buffer[cursor_y][cursor_x:]
                        cursor_x += 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")