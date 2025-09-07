import hashlib
import os
import stat
import getpass
from pathlib import Path

print("Welcome to Nallix")
print(r"""
███╗   ██╗ █████╗ ██╗     ██╗     ██╗██╗  ██╗
████╗  ██║██╔══██╗██║     ██║     ██║╚██╗██╔╝
██╔██╗ ██║███████║██║     ██║     ██║ ╚███╔╝ 
██║╚██╗██║██╔══██║██║     ██║     ██║ ██╔██╗ 
██║ ╚████║██║  ██║███████╗███████╗██║██╔╝ ██╗
╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝╚═╝  ╚═╝""")

def set_secure_permissions(path):
    """Set secure permissions on files and directories"""
    try:
        if os.path.isfile(path):
            os.chmod(path, 0o600)  # Owner read/write only
        elif os.path.isdir(path):
            os.chmod(path, 0o700)  # Owner read/write/execute only
    except Exception as e:
        print(f"Warning: Could not set permissions for {path}: {e}")

user_name = input("What is your username: ")
password = getpass.getpass("Create your password: ")

# Hash the password
hashed_password = hashlib.sha256(password.encode()).hexdigest()

# Get the absolute paths
script_dir = os.path.dirname(os.path.abspath(__file__))
user_root = os.path.abspath(os.path.join(script_dir, '..', 'User'))
user_dir = os.path.join(user_root, user_name)
user_details = os.path.join(user_dir, f"{user_name}_details")
user_home = os.path.join(user_dir, f"{user_name}_home")

# Create user directory
os.makedirs(user_dir, exist_ok=True)

# Create user files
try:
    # Create user_info file with user details
    user_info_path = os.path.join(user_dir, "user_info")
    with open(user_info_path, 'w') as f:
        f.write(f"Username: {user_name}\n")
        f.write(f"Hashed_Password: {hashed_password}\n")
    
    # Create home directory
    home_path = os.path.join(user_dir, "home")
    os.makedirs(home_path, exist_ok=True)
    
    # Create a welcome file in the home directory
    welcome_path = os.path.join(home_path, "welcome")
    with open(welcome_path, 'w') as f:
        f.write(f"Welcome to {user_name}'s home directory.\n")
        f.write("This is your personal space in the Nallix system.\n")
    
    # Set secure permissions
    set_secure_permissions(user_info_path)
    set_secure_permissions(home_path)
    set_secure_permissions(welcome_path)
    set_secure_permissions(user_dir)
    
    print(f"\nUser '{user_name}' created successfully!")
    print(f"User directory: {user_dir}")
    print(f"Home directory: {os.path.join(user_dir, 'home')}")
    
    # Clean up any old user files that might have been created in the wrong location
    old_files = [
        os.path.join(user_root, f"{user_name}.txt"),
        os.path.join(user_root, user_name, f"{user_name}_details"),
        os.path.join(user_root, user_name, f"{user_name}_home")
    ]
    
    for old_file in old_files:
        if os.path.exists(old_file):
            try:
                if os.path.isfile(old_file):
                    os.remove(old_file)
                else:
                    import shutil
                    shutil.rmtree(old_file, ignore_errors=True)
            except Exception as e:
                print(f"Notice: Could not clean up {old_file}: {e}")
    
except Exception as e:
    print(f"Error setting up user: {e}")
    # Clean up partially created directories if something went wrong
    if os.path.exists(user_dir):
        import shutil
        shutil.rmtree(user_dir, ignore_errors=True)
    sys.exit(1)
