import sys
import os
import msvcrt
from typing import List

def get_key():
    try:
        if os.name == 'nt':
            ch = msvcrt.getch()
            if ch in (b'\x00', b'\xe0'):
                ch2 = msvcrt.getch()
                if ch2 == b'H': return 'w'
                elif ch2 == b'P': return 's'
                elif ch2 == b'K': return 'a'
                elif ch2 == b'M': return 'd'
                return ''
            if ch == b'\x08' or ch == b'\x7f': return '\x7f'
            if ch == b'\x1b': return '\x1b'
            if ch == b'\r': return '\r'
            try: return ch.decode('utf-8')
            except: return ''
        else:
            import tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                ch = sys.stdin.read(1)
                if ch == '\x1b':
                    ch = sys.stdin.read(1)
                    if ch == '[':
                        ch = sys.stdin.read(1)
                        if ch == 'A': return 'w'
                        if ch == 'B': return 's'
                        if ch == 'D': return 'a'
                        if ch == 'C': return 'd'
                return ch
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except Exception as e:
        print(f"\nError in get_key: {e}")
        return ''

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_buffer(buffer: List[str], cursor_x: int, cursor_y: int, mode: str, command_mode=False, command=""):
    clear_screen()
    for i, line in enumerate(buffer):
        if i == cursor_y:
            print(line[:cursor_x] + '|' + line[cursor_x:])
        else:
            print(line)
    status = f"-- {mode.upper()} --"
    if command_mode:
        status = f":{command}"
    print(f"\n{status}")
    if not command_mode:
        print("WASD: Move | i: Insert | x: Delete | dd: Delete line | :w to save | :q to quit")

# Global variable to store the current file path
current_file = None

def main():
    global current_file
    
    # Get file path from command line or global variable
    file_path = sys.argv[1] if len(sys.argv) > 1 else current_file
    
    if file_path and os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                buffer = [line.rstrip('\n') for line in f]
            current_file = os.path.abspath(file_path)
        except Exception as e:
            print(f"Error opening file: {e}")
            buffer = [""]
    else:
        buffer = [""]

    cursor_x = 0
    cursor_y = 0
    mode = "normal"
    command_mode = False
    command = ""
    last_key = ""

    while True:
        display_buffer(buffer, cursor_x, cursor_y, mode, command_mode, command)
        key = get_key()

        if command_mode:
            if key == '\r':
                should_exit = False
                
                # Handle :q command
                if command == 'q':
                    should_exit = True
                # Handle :w command
                elif command == 'w':
                    if current_file:
                        try:
                            with open(current_file, 'w') as f:
                                f.write('\n'.join(buffer) + '\n')
                            print(f"Saved to {current_file}")
                        except Exception as e:
                            print(f"Error saving: {e}")
                    else:
                        print("No filename. Use ':w filename' to save")
                # Handle :w filename
                elif command.startswith('w ') and len(command) > 2:
                    save_path = command[2:].strip()
                    try:
                        with open(save_path, 'w') as f:
                            f.write('\n'.join(buffer) + '\n')
                        current_file = os.path.abspath(save_path)
                        print(f"Saved to {current_file}")
                    except Exception as e:
                        print(f"Error saving: {e}")
                # Handle :wq command
                elif command == 'wq':
                    if current_file:
                        try:
                            with open(current_file, 'w') as f:
                                f.write('\n'.join(buffer) + '\n')
                            print(f"Saved to {current_file}")
                            should_exit = True
                        except Exception as e:
                            print(f"Error saving: {e}")
                    else:
                        print("No filename. Use ':w filename' to save")
                # Handle :q! command
                elif command == 'q!':
                    should_exit = True
                
                # Reset command mode
                command_mode = False
                command = ""
                
                # Exit if needed
                if should_exit:
                    return
                    
                continue
            elif key == '\x7f':
                command = command[:-1]
            else:
                command += key
            continue

        if mode == "normal":
            if key == ':':
                command_mode = True
                command = ""
            elif key == 'w' and cursor_y > 0:
                cursor_y -= 1
                cursor_x = min(cursor_x, len(buffer[cursor_y]))
            elif key == 's' and cursor_y < len(buffer) - 1:
                cursor_y += 1
                cursor_x = min(cursor_x, len(buffer[cursor_y]))
            elif key == 'a' and cursor_x > 0:
                cursor_x -= 1
            elif key == 'd' and cursor_x < len(buffer[cursor_y]):
                cursor_x += 1
            elif key == 'i':
                mode = "insert"
            elif key == 'x' and cursor_x < len(buffer[cursor_y]):
                buffer[cursor_y] = buffer[cursor_y][:cursor_x] + buffer[cursor_y][cursor_x + 1:]
            elif key == 'd':
                if last_key == 'd':
                    if len(buffer) > 1:
                        buffer.pop(cursor_y)
                        cursor_y = min(cursor_y, len(buffer) - 1)
                        cursor_x = min(cursor_x, len(buffer[cursor_y]))
            last_key = key

        elif mode == "insert":
            if key == '\x1b':
                mode = "normal"
            elif key == '\r':
                new_line = buffer[cursor_y][cursor_x:]
                buffer[cursor_y] = buffer[cursor_y][:cursor_x]
                buffer.insert(cursor_y + 1, new_line)
                cursor_y += 1
                cursor_x = 0
            elif key == '\x7f':
                if cursor_x > 0:
                    buffer[cursor_y] = buffer[cursor_y][:cursor_x-1] + buffer[cursor_y][cursor_x:]
                    cursor_x -= 1
                elif cursor_y > 0:
                    cursor_x = len(buffer[cursor_y - 1])
                    buffer[cursor_y - 1] += buffer[cursor_y]
                    buffer.pop(cursor_y)
                    cursor_y -= 1
            # Handle text input in insert mode
            if mode == "insert" and key.isprintable() and key not in ['\x1b', '\r']:
                # Ensure the current line exists in the buffer
                while len(buffer) <= cursor_y:
                    buffer.append("")
                # Insert the character at the current position
                buffer[cursor_y] = buffer[cursor_y][:cursor_x] + key + buffer[cursor_y][cursor_x:]
                cursor_x += 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
