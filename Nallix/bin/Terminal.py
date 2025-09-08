import os
import subprocess
import sys
import shutil
import hashlib
import platform
import msvcrt
import json
from datetime import datetime, timedelta
from getpass import getpass
from typing import List, Optional, Tuple

def get_nallix_root():
    """Get the absolute path to the Nallix root directory."""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_user_dir():
    """Get the path to the user home directories."""
    return os.path.join(get_nallix_root(), 'Home')

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

def get_session_file() -> str:
    """Get the path to the session file."""
    return os.path.join(os.path.expanduser("~"), ".nallix_session")

def save_session(username: str, home_dir: str) -> None:
    """Save the current user session."""
    session = {
        'username': username,
        'home_dir': home_dir,
        'timestamp': datetime.now().isoformat()
    }
    with open(get_session_file(), 'w') as f:
        json.dump(session, f)

def clear_session() -> None:
    """Clear the current user session."""
    try:
        if os.path.exists(get_session_file()):
            os.remove(get_session_file())
    except Exception:
        pass

def load_session() -> Tuple[Optional[str], Optional[str]]:
    """Load the saved user session if it exists and is recent."""
    try:
        session_file = get_session_file()
        if not os.path.exists(session_file):
            return None, None
            
        with open(session_file, 'r') as f:
            session = json.load(f)
            
        # Check if session is older than 1 day
        session_time = datetime.fromisoformat(session['timestamp'])
        if datetime.now() - session_time > timedelta(days=1):
            clear_session()
            return None, None
            
        return session['username'], session['home_dir']
    except Exception:
        return None, None

def change_user() -> Tuple[Optional[str], Optional[str]]:
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
            save_session(username, home_dir)
            print(f"Welcome back, {username}!")
            return username, home_dir
        else:
            print("Incorrect password!")
            return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None
        return None, None

def run_nalvim(file_path=None):
    """Run the Nalvim text editor from the correct directory context."""
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    try:
        import nalvim
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

    # Try to load existing session
    current_user, home_dir = load_session()
    if current_user and home_dir:
        username = current_user
        print(f"Welcome back, {username}! (session restored)")
    else:
        current_user = None
        home_dir = get_nallix_root()
        username = "guest"
    current_dir = home_dir

    def run_assemplex(file_path):
        """Run an Assemplex code file."""
        try:
            # Import the run_vm function from Assemplex
            from Assemplex import run_vm
            
            # Read the source code from file
            with open(file_path, 'r') as f:
                source = f.read()
            
            # Run the VM with the source code
            print(f"\n--- Running {os.path.basename(file_path)} ---\n")
            run_vm(source)
            
        except ImportError:
            print("Error: Could not import Assemplex module")
        except FileNotFoundError:
            print(f"Error: File not found: {file_path}")
        except Exception as e:
            print(f"Error running Assemplex code: {e}")

    def print_help():
        print("""Nallix Terminal - Available commands:
  echo <text>       - print text to console
  cd [dir]          - change directory
  pwd               - print working directory
  ls                - list directory contents
  mkdir <dir>       - create a directory
  rmdir <dir>       - remove a directory
  rm <file>         - delete a file
  cat <file>        - display file contents
  cp <src> <dst>    - copy file
  mv <src> <dst>    - move/rename file
  touch <file>      - create an empty file
  head <file>       - display first 10 lines of file
  tail <file>       - display last 10 lines of file
  find <pattern>    - find files matching pattern
  cls               - clear screen
  sudo <command>    - run as superuser
  create user       - create a new user
  change user       - switch active user
  nalvim [file] / nv [file]
  assemplex [file] / asp [file] - run Assemplex code
  help              - show this message
  log out           - sign out current user and switch to guest
  exit              - exit the shell
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
                    print(f"Logging out {username}...")
                    clear_session()
                    sys.exit(0)

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
                        try:
                            path = os.path.join(current_dir, args[0])
                            if os.path.isfile(path):
                                os.remove(path)
                            elif os.path.isdir(path):
                                shutil.rmtree(path)
                        except Exception as e:
                            print(f"rm error: {e}")

                elif cmd == "cat":
                    if args:
                        path = os.path.join(current_dir, args[0])
                        try:
                            with open(path, "r") as f:
                                print(f.read(), end='')
                        except Exception as e:
                            print(f"cat error: {e}")

                elif cmd == "cp":
                    if len(args) >= 2:
                        src = os.path.join(current_dir, args[0])
                        dst = os.path.join(current_dir, args[1])
                        try:
                            if os.path.isdir(src):
                                shutil.copytree(src, dst, dirs_exist_ok=True)
                            else:
                                shutil.copy2(src, dst)
                        except Exception as e:
                            print(f"cp error: {e}")

                elif cmd == "mv":
                    if len(args) >= 2:
                        src = os.path.join(current_dir, args[0])
                        dst = os.path.join(current_dir, args[1])
                        try:
                            shutil.move(src, dst)
                        except Exception as e:
                            print(f"mv error: {e}")

                elif cmd == "touch":
                    if args:
                        try:
                            with open(os.path.join(current_dir, args[0]), 'a'):
                                os.utime(os.path.join(current_dir, args[0]), None)
                        except Exception as e:
                            print(f"touch error: {e}")

                elif cmd == "head":
                    if args:
                        try:
                            with open(os.path.join(current_dir, args[0]), 'r') as f:
                                for i, line in enumerate(f):
                                    if i >= 10:
                                        break
                                    print(line, end='')
                        except Exception as e:
                            print(f"head error: {e}")

                elif cmd == "tail":
                    if args:
                        try:
                            with open(os.path.join(current_dir, args[0]), 'r') as f:
                                lines = f.readlines()
                                for line in lines[-10:]:
                                    print(line, end='')
                        except Exception as e:
                            print(f"tail error: {e}")

                elif cmd == "find":
                    if args:
                        pattern = args[0]
                        try:
                            for root, dirs, files in os.walk(current_dir):
                                for name in files + dirs:
                                    if pattern in name:
                                        print(os.path.join(root, name)[len(current_dir):].lstrip(os.sep))
                        except Exception as e:
                            print(f"find error: {e}")

                elif cmd == "cls":
                    os.system('cls' if os.name == 'nt' else 'clear')

                elif cmd in ("nalvim", "nv"):
                    file_arg = args[0] if args else None
                    path_arg = os.path.join(current_dir, file_arg) if file_arg else None
                    run_nalvim(path_arg)
                    
                elif cmd in ("assemplex", "asp"):
                    if not args:
                        print("Usage: assemplex <filename> or asp <filename>")
                        continue
                    file_arg = args[0]
                    path_arg = os.path.join(current_dir, file_arg)
                    if os.path.exists(path_arg):
                        run_assemplex(path_arg)
                    else:
                        print(f"File not found: {file_arg}")

                elif cmd == "help":
                    print_help()
                    
                elif cmd == "log" and len(args) > 0 and args[0] == "out":
                    if current_user:
                        print(f"Logging out {username}...")
                        current_user = None
                        home_dir = get_nallix_root()
                        username = "guest"
                        current_dir = home_dir
                        clear_session()
                    else:
                        print("No user is currently logged in.")

                else:
                    subprocess.run(command, shell=True, cwd=current_dir)
        
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except EOFError:
            print("\nEOF received, exiting.")
            break

if __name__ == "__main__":
    run_shell()
