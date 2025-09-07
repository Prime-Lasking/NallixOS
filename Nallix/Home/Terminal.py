import os
import subprocess
import sys
import shutil
import hashlib
from getpass import getpass

def get_nallix_root():
    """Get the absolute path to the Nallix root directory"""
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def get_user_dir():
    """Get the path to the User directory"""
    return os.path.join(get_nallix_root(), 'User')

def verify_sudo(user_name):
    """Verify sudo password for a user"""
    user_file = os.path.join(get_user_dir(), user_name, f"{user_name}_details")
    
    try:
        # Read stored password hash
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
        
        # Give 3 attempts to enter the correct password
        attempts = 3
        while attempts > 0:
            sudo_password = getpass.getpass(f"[sudo] password for {user_name}: ")
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
    """Create a new user"""
    user_name = input("Enter new username: ")
    password = getpass("Enter password: ")
    
    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    
    # Set up paths
    user_dir = os.path.join(get_user_dir(), user_name)
    user_info_path = os.path.join(user_dir, "user_info")
    home_path = os.path.join(user_dir, "home")
    
    try:
        # Create user directory and home directory
        os.makedirs(user_dir, exist_ok=True)
        os.makedirs(home_path, exist_ok=True)
        
        # Create user_info file
        with open(user_info_path, 'w') as f:
            f.write(f"Username: {user_name}\n")
            f.write(f"Hashed_Password: {hashed_password}\n")
        
        # Create welcome file in home directory
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
        # Clean up partially created directories if something went wrong
        if os.path.exists(user_dir):
            import shutil
            shutil.rmtree(user_dir, ignore_errors=True)
        return None

def change_user():
    """Change the current user and return user info and home directory"""
    user_name = input("Enter username: ")
    password = getpass("Enter password: ")
    
    user_dir = os.path.join(get_user_dir(), user_name)
    user_info_path = os.path.join(user_dir, "user_info")
    home_dir = os.path.join(user_dir, "home")
    
    try:
        if not os.path.exists(user_info_path):
            print("User does not exist.")
            return None, None
            
        with open(user_info_path, 'r') as f:
            stored_username = f.readline().strip().split(': ')[1]
            stored_hash = f.readline().strip().split(': ')[1]
            
        # Verify password
        if hashlib.sha256(password.encode()).hexdigest() == stored_hash:
            print(f"Welcome back, {user_name}!")
            return user_name, home_dir
        else:
            print("Incorrect password!")
            return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None

def run_shell():
    print("Nallix Terminal (type 'exit' or Ctrl+C to quit)")
    print("Type 'help' for available commands\n")

    current_user = None
    current_dir = get_nallix_root()  # Start in Nallix root directory
    
    # If user logs in via command line args, change to their home directory
    if len(sys.argv) > 1 and sys.argv[1] == "--login":
        if len(sys.argv) > 2:
            username = sys.argv[2]
            password = getpass("Enter password: ")
            current_user, home_dir = change_user()
            if current_user and home_dir:
                current_dir = home_dir
    os.chdir(current_dir)

    def print_help():
        user_status = f"{current_user}" if current_user else "guest"
        print(f"""Nallix Terminal - Available commands{user_status}:
  echo [text]       - print text
  ls                - displays directory contents
  cd [dir]          - change directory
  pwd               - print current directory
  mkdir [dir]       - create a directory
  rmdir [dir]       - remove an empty directory
  del/rm [file]     - delete a file
  type [file]       - display file contents
  copy [src] [dst]  - copy file
  move [src] [dst]  - move/rename file
  cls               - clear screen
  sudo [command]    - run command with elevated privileges
  help              - show this help
  exit              - exit the shell
  create user       - Create a new user account
  change user       - Switch to a different user
  sudo [command]    - Execute a command with elevated privileges
  exit              - exit the shell

Current directory: {os.path.relpath(current_dir, get_nallix_root())}
Other commands run via Windows shell (cmd.exe).
Use multiline input: enter blank line to run.
""")

    while True:
        try:
            # Display prompt with relative path and username
            rel_path = os.path.relpath(current_dir, get_nallix_root())
            prompt = f"{current_user}@{rel_path}> " if current_user else f"guest@{rel_path}> "
            print(prompt, end='', flush=True)
            
            # Multiline input
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

            commands = command_block.split('\n')

            for command in commands:
                parts = command.strip().split()
                if not parts:
                    continue
                cmd = parts[0].lower()
                args = parts[1:]

                # Built-in commands
                if cmd == "sudo":
                    if not current_user:
                        print("Please log in first to use sudo")
                        continue
                    if not args:
                        print("Usage: sudo <command>")
                        continue
                    
                    # Always verify sudo password
                    if not verify_sudo(current_user):
                        continue
                        
                    # Execute the command with sudo privileges
                    try:
                        print(f"[sudo] executing: {' '.join(args)}")
                        result = subprocess.run(
                            " ".join(args),
                            shell=True,
                            cwd=current_dir,
                            text=True,
                            capture_output=True
                        )
                        
                        # Print command output if any
                        if result.stdout:
                            print(result.stdout, end='')
                        if result.stderr:
                            print(result.stderr, end='', file=sys.stderr)
                            
                    except Exception as e:
                        print(f"sudo: error executing command: {e}")
                    
                elif cmd == "create" and args and args[0].lower() == "user":
                    if current_user and not sudo_active:
                        print("Please use 'sudo create user' to create a new user.")
                    else:
                        current_user = create_user()
                        if current_user:
                            # After creating a user, set the current directory to their home
                            current_dir = os.path.join(get_user_dir(), current_user, "home")
                elif cmd == "change" and args and args[0].lower() == "user":
                    if current_user:
                        print(f"Logging out {current_user}")
                        current_user = None
                        sudo_active = False
                    current_user, home_dir = change_user()
                    if current_user and home_dir:
                        current_dir = home_dir
                elif cmd == "echo":
                    print(" ".join(args))
                elif cmd == "cd":
                    if args:
                        try:
                            new_dir = args[0]
                            if not os.path.isabs(new_dir):
                                new_dir = os.path.join(current_dir, new_dir)
                            # Don't allow navigating outside Nallix directory
                            new_dir = os.path.normpath(os.path.abspath(new_dir))
                            if not new_dir.startswith(get_nallix_root()):
                                print("Error: Cannot navigate outside Nallix directory")
                                continue
                            os.chdir(new_dir)
                            current_dir = os.getcwd()
                        except Exception as e:
                            print(f"cd error: {e}")
                    else:
                        # Go to user's home directory if logged in, else Nallix root
                        if current_user:
                            user_home = os.path.join(get_user_dir(), current_user)
                            os.makedirs(user_home, exist_ok=True)
                            os.chdir(user_home)
                            current_dir = user_home
                        else:
                            os.chdir(get_nallix_root())
                            current_dir = get_nallix_root()
                elif cmd == "pwd":
                    print(current_dir)
                elif cmd == "mkdir":
                    if not args:
                        print("mkdir error: missing directory name")
                    else:
                        try:
                            path = args[0]
                            if not os.path.isabs(path):
                                path = os.path.join(current_dir, path)
                            os.makedirs(path, exist_ok=True)
                        except Exception as e:
                            print(f"mkdir error: {e}")
                elif cmd == "rmdir":
                    if not args:
                        print("rmdir error: missing directory name")
                    else:
                        try:
                            path = args[0]
                            if not os.path.isabs(path):
                                path = os.path.join(current_dir, path)
                            os.rmdir(path)
                        except Exception as e:
                            print(f"rmdir error: {e}")
                elif cmd in ("del", "rm"):
                    if not args:
                        print(f"{cmd} error: missing filename")
                    else:
                        try:
                            path = args[0]
                            if not os.path.isabs(path):
                                path = os.path.join(current_dir, path)
                            os.remove(path)
                        except Exception as e:
                            print(f"{cmd} error: {e}")
                elif cmd == "type":
                    if not args:
                        print("type error: missing filename")
                    else:
                        try:
                            path = args[0]
                            if not os.path.isabs(path):
                                path = os.path.join(current_dir, path)
                            with open(path, "r") as f:
                                print(f.read())
                        except Exception as e:
                            print(f"type error: {e}")
                elif cmd == "copy":
                    if len(args) < 2:
                        print("copy error: need source and destination")
                    else:
                        try:
                            src, dst = args[0], args[1]
                            if not os.path.isabs(src):
                                src = os.path.join(current_dir, src)
                            if not os.path.isabs(dst):
                                dst = os.path.join(current_dir, dst)
                            shutil.copy2(src, dst)
                        except Exception as e:
                            print(f"copy error: {e}")
                elif cmd == "move":
                    if len(args) < 2:
                        print("move error: need source and destination")
                    else:
                        try:
                            src, dst = args[0], args[1]
                            if not os.path.isabs(src):
                                src = os.path.join(current_dir, src)
                            if not os.path.isabs(dst):
                                dst = os.path.join(current_dir, dst)
                            shutil.move(src, dst)
                        except Exception as e:
                            print(f"move error: {e}")
                elif cmd == "cls":
                    os.system('cls')
                elif cmd == "ls":
                   os.system('dir')
                elif cmd == "help":
                    print_help()
                else:
                    # Fallback to Windows shell (cmd.exe)
                    try:
                        completed = subprocess.run(command, shell=True, cwd=current_dir)
                        if completed.returncode != 0:
                            print(f"Command failed with exit code {completed.returncode}")
                    except Exception as e:
                        print(f"Error running command: {e}")

        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except EOFError:
            print("\nEOF received, exiting.")
            break

if __name__ == "__main__":
    run_shell()
