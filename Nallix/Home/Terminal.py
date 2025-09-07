import os
import subprocess
import sys
import shutil
import hashlib
import platform
import msvcrt
from getpass import getpass
from typing import List

def get_nallix_root():
    """Get the absolute path to the Nallix root directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_user_dir():
    """Get the path to the User directory."""
    return os.path.join(get_nallix_root(), 'User')

def verify_sudo(user_name):
    """Verify sudo password for a user."""
    user_file = os.path.join(get_user_dir(), user_name, f"{user_name}_details")
    try:
        with open(user_file, 'r') as f:
            lines = f.readlines()
        stored_hash = None
        for line in lines:
            if line.startswith('Hashed_Password:'):
                stored_hash = line.split(': ')[1].strip()
                break
        if not stored_hash:
            print("Error: Could not verify credentials")
            return False

        attempts = 3
        while attempts > 0:
            sudo_password = getpass(f"[sudo] password for {user_name}: ")
            input_hash = hashlib.sha256(sudo_password.encode()).hexdigest()
            if input_hash == stored_hash:
                return True
            attempts -= 1
            if attempts > 0:
                print(f"Sorry, try again. {attempts} attempts remaining.")
            else:
                print("sudo: 3 incorrect password attempts")
                return False
    except Exception as e:
        print(f"Error verifying sudo: {e}")
        return False

def create_user():
    """Create a new user."""
    user_name = input("Enter new username: ")
    password = getpass("Enter password: ")

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    user_dir = os.path.join(get_user_dir(), user_name)
    user_info_path = os.path.join(user_dir, "user_info")
    home_path = os.path.join(user_dir, "home")

    try:
        os.makedirs(user_dir, exist_ok=True)
        os.makedirs(home_path, exist_ok=True)

        with open(user_info_path, 'w') as f:
            f.write(f"Username: {user_name}\n")
            f.write(f"Hashed_Password: {hashed_password}\n")

        welcome_path = os.path.join(home_path, "welcome")
        with open(welcome_path, 'w') as f:
            f.write(f"Welcome to {user_name}'s home directory.\n")
            f.write("This is your personal space in the Nallix system.\n")

        print(f"User '{user_name}' created successfully!")
        print(f"User directory: {user_dir}")
        print(f"Home directory: {home_path}")
        return user_name
    except Exception as e:
        print(f"Error creating user: {e}")
        if os.path.exists(user_dir):
            shutil.rmtree(user_dir, ignore_errors=True)
        return None

def change_user():
    """Change user and return (username, home_dir)."""
    try:
        username = input("Enter username: ")
        user_dir = os.path.join(get_user_dir(), username)
        user_info_path = os.path.join(user_dir, "user_info")
        if not os.path.exists(user_info_path):
            print("User does not exist.")
            return None, None

        password = getpass("Enter password: ")
        with open(user_info_path, 'r') as f:
            stored_username = f.readline().strip().split(': ')[1]
            stored_hash = f.readline().strip().split(': ')[1]
        if hashlib.sha256(password.encode()).hexdigest() == stored_hash:
            home_dir = os.path.join(user_dir, 'home')
            print(f"Welcome back, {username}!")
            return username, home_dir
        else:
            print("Incorrect password!")
            return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def run_nalvim(file_path=None):
    """Run the Nalvim text editor from the correct directory context."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    try:
        from Nallix.Home import nalvim
    except ImportError as e:
        print(f"Error: Could not import nalvim from Home.\nDetails: {e}")
        return

    if file_path:
        file_path = os.path.abspath(file_path)
        sys.argv = [sys.argv[0], file_path]
    else:
        sys.argv = [sys.argv[0]]

    try:
        nalvim.main()
    except Exception as e:
        print(f"Error running nalvim: {e}")

def run_shell():
    print("Nallix Terminal (type 'exit' or Ctrl+C to quit)")
    print("Type 'help' for available commands\n")

    current_user = None
    current_dir = get_nallix_root()
    os.chdir(current_dir)

    def print_help():
        print(f"""Nallix Terminal - Available commands:
  echo [text]
  ls / cd / pwd / mkdir / rmdir / del / type / copy / move / cls
  sudo [command]       – run command as root
  create user          – create a new user
  change user          – switch active user
  nalvim [file] / nv [file]
  help                 – show this message
  exit                 – exit the shell
""")

    while True:
        try:
            rel_path = os.path.relpath(current_dir, get_nallix_root())
            prompt = f"{current_user or 'guest'}@{rel_path}> "
            print(prompt, end='', flush=True)

            lines = []
            while True:
                line = input()
                if line.strip() == "" and lines:
                    break
                if line.strip().lower() == "exit":
                    print("Bye!")
                    return
                lines.append(line)

            command_block = "\n".join(lines).strip()
            if not command_block:
                continue

            for command in command_block.split('\n'):
                parts = command.strip().split()
                if not parts:
                    continue

                cmd = parts[0].lower()
                args = parts[1:]

                if cmd == "sudo":
                    if not current_user:
                        print("Please log in first to use sudo")
                        continue
                    if not args:
                        print("Usage: sudo <command>")
                        continue
                    if not verify_sudo(current_user):
                        continue
                    result = subprocess.run(" ".join(args), shell=True, cwd=current_dir, text=True, capture_output=True)
                    if result.stdout:
                        print(result.stdout, end='')
                    if result.stderr:
                        print(result.stderr, end='', file=sys.stderr)

                elif cmd == "create" and args and args[0].lower() == "user":
                    current_user = create_user()

                elif cmd == "change" and args and args[0].lower() == "user":
                    current_user, home_dir = change_user()
                    if current_user and home_dir:
                        current_dir = home_dir
                        os.chdir(current_dir)

                elif cmd == "echo":
                    print(" ".join(args))

                elif cmd == "cd":
                    target = args[0] if args else None
                    if target:
                        new_dir = os.path.abspath(os.path.join(current_dir, target))
                        if not new_dir.startswith(get_nallix_root()):
                            print("Error: Cannot navigate outside Nallix directory")
                            continue
                        if os.path.isdir(new_dir):
                            current_dir = new_dir
                            os.chdir(current_dir)
                        else:
                            print("cd error: directory not found")
                    elif current_user:
                        home_dir = os.path.join(get_user_dir(), current_user, 'home')
                        current_dir = home_dir
                        os.chdir(current_dir)
                    else:
                        current_dir = get_nallix_root()
                        os.chdir(current_dir)

                elif cmd == "pwd":
                    print(current_dir)

                elif cmd == "ls":
                    for item in os.listdir(current_dir):
                        print(item)

                elif cmd == "mkdir":
                    if args:
                        os.makedirs(os.path.join(current_dir, args[0]), exist_ok=True)

                elif cmd == "rmdir":
                    if args:
                        os.rmdir(os.path.join(current_dir, args[0]))

                elif cmd in ("del", "rm"):
                    if args:
                        os.remove(os.path.join(current_dir, args[0]))

                elif cmd == "type":
                    if args:
                        path = os.path.join(current_dir, args[0])
                        try:
                            with open(path, "r") as f:
                                print(f.read())
                        except Exception as e:
                            print(f"type error: {e}")

                elif cmd == "copy":
                    if len(args) >= 2:
                        src = os.path.join(current_dir, args[0])
                        dst = os.path.join(current_dir, args[1])
                        try:
                            shutil.copy2(src, dst)
                        except Exception as e:
                            print(f"copy error: {e}")

                elif cmd == "move":
                    if len(args) >= 2:
                        src = os.path.join(current_dir, args[0])
                        dst = os.path.join(current_dir, args[1])
                        try:
                            shutil.move(src, dst)
                        except Exception as e:
                            print(f"move error: {e}")

                elif cmd == "cls":
                    os.system('cls' if os.name == 'nt' else 'clear')

                elif cmd in ("nalvim", "nv"):
                    file_arg = args[0] if args else None
                    path_arg = os.path.join(current_dir, file_arg) if file_arg else None
                    run_nalvim(path_arg)

                elif cmd == "help":
                    print_help()

                elif cmd == "exit":
                    print("Bye!")
                    return

                else:
                    subprocess.run(command, shell=True, cwd=current_dir)
        
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except EOFError:
            print("\nEOF received, exiting.")
            break

if __name__ == "__main__":
    run_shell()
