import os
import subprocess
import sys
import shutil
import hashlib
import json
from datetime import datetime, timedelta
from getpass import getpass
from typing import Tuple, Optional

# Constants
SESSION_TIMEOUT = 3600  # 1 hour in seconds

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
    """Create a new user with hashed password storage."""
    try:
        print("Create a new user")
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty")
            return
            
        user_dir = os.path.join(get_user_dir(), username)
        if os.path.exists(user_dir):
            print(f"User '{username}' already exists")
            return
            
        # Set password with validation
        while True:
            password = getpass("Enter password: ")
            if not password:
                print("Password cannot be empty")
                continue
                
            confirm = getpass("Confirm password: ")
            if password == confirm:
                break
            print("Passwords do not match, try again")
            
        # Create user directory and home
        home_path = os.path.join(user_dir, 'home')
        os.makedirs(user_dir, exist_ok=True)
        os.makedirs(home_path, exist_ok=True)
        
        # Store user details securely
        user_file = os.path.join(user_dir, f"{username}_details")
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        
        with open(user_file, 'w') as f:
            f.write(f"Username: {username}\n")
            f.write(f"Hashed_Password: {hashed_pw}\n")
            f.write(f"Created: {datetime.now().isoformat()}\n")
            
        # Create welcome file
        welcome_path = os.path.join(home_path, "welcome")
        with open(welcome_path, 'w') as f:
            f.write(f"Welcome to {username}'s home directory.\n")
            f.write("This is your personal space in the Nallix system.\n")
            
        print(f"User '{username}' created successfully!")
        print(f"User directory: {user_dir}")
        print(f"Home directory: {home_path}")
        return username
        
    except Exception as e:
        print(f"Error creating user: {e}")
        # Clean up if user directory was created but user creation failed
        if 'user_dir' in locals() and os.path.exists(user_dir):
            shutil.rmtree(user_dir, ignore_errors=True)
        return None

def get_session_file():
    """Get the path to the session file."""
    session_dir = os.path.join(get_nallix_root(), '.nallix')
    os.makedirs(session_dir, exist_ok=True)
    return os.path.join(session_dir, 'session')

def save_session(username: str, home_dir: str):
    """Save the current user session with timestamp."""
    try:
        session = {
            'username': username,
            'home_dir': home_dir,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0'
        }
        session_file = get_session_file()
        temp_file = f"{session_file}.tmp"
        
        # Write to temp file first, then rename (atomic operation)
        with open(temp_file, 'w') as f:
            json.dump(session, f)
            
        # On Windows, we need to remove the destination file first if it exists
        if os.path.exists(session_file):
            os.replace(temp_file, session_file)
        else:
            os.rename(temp_file, session_file)
            
    except Exception as e:
        print(f"Error saving session: {e}")
        # Clean up temp file if it exists
        if 'temp_file' in locals() and os.path.exists(temp_file):
            os.remove(temp_file)

def clear_session():
    """Clear the current user session."""
    try:
        if os.path.exists(get_session_file()):
            os.remove(get_session_file())
    except Exception:
        pass

def load_session() -> Tuple[Optional[str], Optional[str]]:
    """Load the saved user session if it exists and hasn't timed out."""
    session_file = get_session_file()
    if not os.path.exists(session_file):
        return None, None
        
    try:
        with open(session_file, 'r') as f:
            session = json.load(f)
            
        # Check session version
        if session.get('version') != '1.0':
            print("Warning: Session format is outdated. Please log in again.")
            return None, None
            
        # Check if session is still valid
        session_time = datetime.fromisoformat(session['timestamp'])
        if (datetime.now() - session_time) > timedelta(seconds=SESSION_TIMEOUT):
            print("Session expired. Please log in again.")
            return None, None
            
        # Verify user directory exists
        if not os.path.isdir(session['home_dir']):
            print("User directory not found. Please log in again.")
            return None, None
            
        return session['username'], session['home_dir']
        
    except json.JSONDecodeError:
        print("Error: Corrupted session file")
        return None, None
    except Exception as e:
        print(f"Error loading session: {e}")
        return None, None

def create_user():
    """Create a new user with hashed password storage."""
    try:
        print("Create a new user")
        username = input("Enter username: ").strip()
        if not username:
            print("Username cannot be empty")
            return
            
        user_dir = os.path.join(get_user_dir(), username)
        if os.path.exists(user_dir):
            print(f"User '{username}' already exists")
            return
            
        os.makedirs(user_dir, exist_ok=True)
        
        # Set password with validation
        while True:
            password = getpass("Enter password: ")
            if not password:
                print("Password cannot be empty")
                continue
                
            confirm = getpass("Confirm password: ")
            if password == confirm:
                break
            print("Passwords do not match, try again")
            
        # Store user details securely
        user_file = os.path.join(user_dir, f"{username}_details")
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        
        with open(user_file, 'w') as f:
            f.write(f"Username: {username}\n")
            f.write(f"Hashed_Password: {hashed_pw}\n")
            f.write(f"Created: {datetime.now().isoformat()}\n")
            
        print(f"User '{username}' created successfully!")
        
    except Exception as e:
        print(f"Error creating user: {e}")
        # Clean up if user directory was created but user creation failed
        if 'user_dir' in locals() and os.path.exists(user_dir):
            shutil.rmtree(user_dir)

def change_user() -> Tuple[Optional[str], Optional[str]]:
    """Change user and return (username, home_dir)."""
    try:
        username = input("Enter username: ")
        user_dir = os.path.join(get_user_dir(), username)
        user_info_path = os.path.join(user_dir, f"{username}_details")
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

def run_nalvim(file_path=None):
    """Run the Nalvim text editor from the correct directory context."""
    import sys
    import os
    
    # Save current directory and change to Nallix root
    original_dir = os.getcwd()
    os.chdir(get_nallix_root())
    
    # Import after changing directory to ensure relative imports work
    from bin import nalvim
    
    # Set up command line arguments
    if file_path:
        sys.argv = [sys.argv[0], file_path]
    else:
        sys.argv = [sys.argv[0]]

    try:
        nalvim.main()
    except Exception as e:
        print(f"Error running nalvim: {e}")
    finally:
        # Restore original directory
        os.chdir(original_dir)

def run_command(command):
    """Execute a single Nallix command and return the output"""
    import subprocess
    import os
    import sys
    
    if not command:
        return ""
        
    cmd = command.split()[0].lower()
    args = command.split()[1:] if len(command.split()) > 1 else []
    
    # Handle built-in commands
    if cmd == 'pwd':
        return os.getcwd()
    elif cmd == 'clear':
        return "\n" * 100  # Hack to clear the screen
    elif cmd == 'ls':
        try:
            path = args[0] if args else '.'
            items = os.listdir(path)
            output = []
            for item in sorted(items, key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower())):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    output.append(f"{item}/")
                elif os.access(full_path, os.X_OK):
                    output.append(f"{item}*")
                else:
                    output.append(item)
            return '\n'.join(output)
        except Exception as e:
            return f"ls: {str(e)}"
    elif cmd == 'cd':
        try:
            target = ' '.join(args).strip('"\'')
            if not target:
                target = os.path.expanduser('~')
            os.chdir(target)
            return os.getcwd()
        except Exception as e:
            return f"cd: {str(e)}"
    elif cmd == 'kex':
        # This will be handled by the desktop environment
        return "Launching Nallix Desktop..."
    # Removed whoami command as username is now shown in prompt
    
    # Try to run as system command
    try:
        result = subprocess.getoutput(command)
        return result
    except Exception as e:
        return f"Command error: {str(e)}"

def setup_guest_user():
    """Set up the guest user directory if it doesn't exist."""
    guest_dir = os.path.join(get_nallix_root(), 'Home', 'guest')
    guest_home = os.path.join(guest_dir, 'home')
    
    # Create guest directory structure if it doesn't exist
    if not os.path.exists(guest_home):
        os.makedirs(guest_home, exist_ok=True)
        
        # Create a welcome file
        welcome_path = os.path.join(guest_home, 'welcome.txt')
        with open(welcome_path, 'w') as f:
            f.write("Welcome to Nallix Terminal (Guest Mode)\n")
            f.write("Type 'help' for available commands\n")
    
    return 'guest', guest_home

def run_shell():
    print("Nallix Terminal (type 'exit' or Ctrl+C to quit)")
    print("Type 'help' for available commands\n")

    # Try to load existing session or use guest
    current_user, home_dir = load_session()
    if not current_user or not home_dir:
        current_user, home_dir = setup_guest_user()
        print("Logged in as guest. Type 'help' for available commands")
    else:
        print(f"Welcome back, {current_user}! (session restored)")
    
    current_dir = home_dir
    os.chdir(current_dir)  # Set the working directory

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
  cd [directory]    - Change directory
  ls [path]         - List directory contents
  pwd               - Show current directory
  clear             - Clear the screen
  exit/quit         - Exit the terminal
  kex               - Launch Nallix Desktop
  help              - Show this help message
  
File Operations:
  cat <file>        - Display file contents
  cp <src> <dst>    - Copy file
  mv <src> <dst>    - Move/rename file
  rm <file>         - Delete a file
  mkdir <dir>       - Create a directory
  rmdir <dir>       - Remove a directory
  touch <file>      - Create an empty file
  
System:
  echo <text>       - Print text to console
  find <pattern>    - Find files matching pattern
  sudo <command>    - Run as superuser
  
Nallix Specific:
  nalvim [file]     - Open Nalvim editor
  nv [file]         - Alias for nalvim
  assemplex [file]  - Run Assemplex code
  asp [file]        - Alias for assemplex
  
User Management:
  create user       - Create a new user
  change user       - Switch active user
  log out           - sign out current user and switch to guest
  exit              - exit the shell
""")

    # Function to get the current prompt
    def get_prompt():
        rel_path = os.path.relpath(current_dir, get_nallix_root())
        # Add color to the username and path
        username = f"\033[92m{current_user or 'guest'}\033[0m"  # Green username
        path = f"\033[94m{rel_path}\033[0m"  # Blue path
        return f"{username}@{path}> "

    while True:
        try:
            print(get_prompt(), end='', flush=True)

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
                    result = subprocess.run(" ".join(args), shell=True, cwd=current_dir, text=True, capture_output=True)
                    if result.stdout:
                        print(result.stdout, end='')
                    if result.stderr:
                        print(result.stderr, end='', file=sys.stderr)

                elif cmd == "create" and args and args[0].lower() == "user":
                    create_user()
                    
                elif cmd == "change" and args and args[0].lower() == "user":
                    new_user, new_home = change_user()
                    if new_user and new_home:
                        current_user = new_user
                        home_dir = new_home
                        current_dir = home_dir
                        os.chdir(current_dir)

                elif cmd in ['exit', 'quit']:
                    if current_user:
                        print(f"Logging out {username}...")
                        current_user = None
                        home_dir = get_nallix_root()
                        username = "guest"
                        current_dir = home_dir
                        clear_session()
                    else:
                        break

                elif cmd == "help":
                    print_help()

                elif cmd in ["clear", "cls"]:
                    os.system('cls' if os.name == 'nt' else 'clear')

                elif cmd == "cd":
                    try:
                        if not args:
                            os.chdir(home_dir)
                            current_dir = home_dir
                        else:
                            target = args[0].strip('"\'')
                            if target == "~":
                                os.chdir(home_dir)
                                current_dir = home_dir
                            else:
                                new_dir = os.path.abspath(os.path.join(current_dir, target))
                                if not new_dir.startswith(get_nallix_root()):
                                    print("Error: Cannot navigate outside Nallix directory")
                                    continue
                                os.chdir(new_dir)
                                current_dir = new_dir
                    except Exception as e:
                        print(f"cd: {e}")
                        print(item)
                    except Exception as e:
                        print(f"ls: {e}")

                elif cmd == "echo":
                    print(" ".join(args))

                elif cmd == "mkdir":
                    if args:
                        os.makedirs(os.path.join(current_dir, args[0]), exist_ok=True)

                elif cmd == "rmdir":
                    if args:
                        os.rmdir(os.path.join(current_dir, args[0]))

                # File operations
                elif cmd in ("del", "rm"):
                    if not args:
                        print("Usage: rm <file>")
                        continue
                    try:
                        path = os.path.join(current_dir, args[0])
                        if os.path.isfile(path) or os.path.islink(path):
                            os.remove(path)
                        elif os.path.isdir(path):
                            shutil.rmtree(path)
                        else:
                            print(f"rm: cannot remove '{args[0]}': No such file or directory")
                    except Exception as e:
                        print(f"rm: {e}")

                elif cmd == "cp" and len(args) >= 2:
                    try:
                        src = os.path.join(current_dir, args[0])
                        dst = os.path.join(current_dir, args[1])
                        if os.path.isdir(src):
                            shutil.copytree(src, dst, dirs_exist_ok=True)
                        else:
                            shutil.copy2(src, dst)
                    except Exception as e:
                        print(f"cp: {e}")

                elif cmd == "mv" and len(args) >= 2:
                    try:
                        src = os.path.join(current_dir, args[0])
                        dst = os.path.join(current_dir, args[1])
                        shutil.move(src, dst)
                    except Exception as e:
                        print(f"mv: {e}")

                elif cmd == "touch" and args:
                    try:
                        with open(os.path.join(current_dir, args[0]), 'a'):
                            os.utime(os.path.join(current_dir, args[0]), None)
                    except Exception as e:
                        print(f"touch: {e}")

                elif cmd == "cat" and args:
                    try:
                        with open(os.path.join(current_dir, args[0]), 'r') as f:
                            print(f.read())
                    except Exception as e:
                        print(f"cat: {e}")

                elif cmd == "find" and args:
                    try:
                        search_dir = current_dir
                        pattern = args[0]
                        if len(args) > 1:
                            search_dir = os.path.join(current_dir, args[1])
                        
                        for root, dirs, files in os.walk(search_dir):
                            for name in files + dirs:
                                if pattern.lower() in name.lower():
                                    print(os.path.relpath(os.path.join(root, name), current_dir))
                    except Exception as e:
                        print(f"find: {e}")

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

                elif cmd == "kex":
                    try:
                        # Check if we're running in desktop mode
                        if 'NALLIX_DESKTOP' in os.environ:
                            print("Already in Nallix Desktop environment.")
                            continue
                            
                        print("Launching Nallix Desktop...")
                        
                        # Launch desktop in a separate process
                        if sys.platform == 'win32':
                            python_exe = sys.executable
                            desktop_path = os.path.join(os.path.dirname(__file__), 'desktop.py')
                            subprocess.Popen([python_exe, desktop_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
                        else:
                            # For Unix-like systems
                            python_exe = sys.executable
                            desktop_path = os.path.join(os.path.dirname(__file__), 'desktop.py')
                            subprocess.Popen([python_exe, desktop_path], 
                                          stdout=subprocess.PIPE, 
                                          stderr=subprocess.PIPE,
                                          start_new_session=True)
                        
                        print("Nallix Desktop launched in a new window.")
                        break  # Exit the terminal loop when desktop starts
                    except ImportError as e:
                        print(f"Error: Could not import desktop module: {e}")
                    except Exception as e:
                        print(f"Error launching desktop: {e}")
                
                # Fall back to system command if not handled above
                elif cmd not in ["sudo", "create", "change"]:  # Skip already handled commands
                    try:
                        result = subprocess.getoutput(command)
                        if result:
                            print(result)
                    except Exception as e:
                        print(f"Command error: {e}")
        
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except EOFError:
            print("\nEOF received, exiting.")
            break

if __name__ == "__main__":
    run_shell()
