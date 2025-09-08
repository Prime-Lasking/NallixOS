import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser, font
import os
import sys
import json
import platform
from datetime import datetime
from PIL import Image, ImageTk
import subprocess
import socket
import psutil
import threading

# Import Nallix terminal
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Terminal import run_shell

class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Nallix Desktop")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg='#1e1e1e')
        
        # Set up desktop background
        self.setup_desktop()
        
        # Set up taskbar
        self.setup_taskbar()
        
        # Set up start menu (initially hidden)
        self.setup_start_menu()
        
        # Add some desktop icons
        self.add_desktop_icons()
        
        # Bind right-click for desktop menu
        self.root.bind("<Button-3>", self.show_desktop_menu)
        
    def setup_desktop(self):
        # Desktop frame that fills the window
        self.desktop = tk.Canvas(self.root, highlightthickness=0)
        self.desktop.pack(fill='both', expand=True)
        
        # Default wallpaper settings
        self.wallpaper_path = None
        self.wallpaper_image = None
        self.wallpaper_photo = None
        self.wallpaper_label = None
        
        # Set default wallpaper
        self.set_wallpaper()
        
    def setup_taskbar(self):
        # Taskbar frame at the bottom
        self.taskbar = tk.Frame(self.root, bg='#2d2d2d', height=40)
        self.taskbar.pack(side='bottom', fill='x')
        
        # Start button
        self.start_btn = tk.Button(
            self.taskbar,
            text="Start",
            bg='#2d2d2d',
            fg='white',
            border=0,
            command=self.toggle_start_menu
        )
        self.start_btn.pack(side='left', padx=5)
        
        # Taskbar applications area
        self.taskbar_apps = tk.Frame(self.taskbar, bg='#2d2d2d')
        self.taskbar_apps.pack(side='left', fill='both', expand=True)
        
        # System tray (time, date, etc.)
        self.setup_system_tray()
    
    def setup_system_tray(self):
        # System tray on the right side of taskbar
        system_tray = tk.Frame(self.taskbar, bg='#2d2d2d')
        system_tray.pack(side='right', padx=5)
        
        # Display time
        self.time_label = tk.Label(
            system_tray,
            text=self.get_current_time(),
            bg='#2d2d2d',
            fg='white',
            font=('Arial', 10)
        )
        self.time_label.pack(side='right', padx=5)
        
        # Update time every second
        self.update_time()
    
    def get_current_time(self):
        from datetime import datetime
        return datetime.now().strftime("%H:%M %p")
    
    def update_time(self):
        self.time_label.config(text=self.get_current_time())
        self.root.after(1000, self.update_time)
        
    def set_wallpaper(self, image_path=None):
        """Set the desktop wallpaper."""
        try:
            if self.wallpaper_label:
                self.wallpaper_label.destroy()
                
            if image_path and os.path.exists(image_path):
                self.wallpaper_path = image_path
                self.wallpaper_image = Image.open(image_path)
                
                # Resize image to fit the screen while maintaining aspect ratio
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                self.wallpaper_image.thumbnail((screen_width, screen_height), Image.LANCZOS)
                
                # Center the image
                img_width, img_height = self.wallpaper_image.size
                x = (screen_width - img_width) // 2
                y = (screen_height - img_height) // 2
                
                # Create a blank image with the wallpaper
                bg_image = Image.new('RGB', (screen_width, screen_height), '#1e1e1e')
                bg_image.paste(self.wallpaper_image, (x, y))
                
                self.wallpaper_photo = ImageTk.PhotoImage(bg_image)
                self.wallpaper_label = tk.Label(self.desktop, image=self.wallpaper_photo)
                self.wallpaper_label.place(x=0, y=0, relwidth=1, relheight=1)
                self.wallpaper_label.lower()  # Move to bottom layer
                
                # Save wallpaper path to config
                self.save_settings()
            else:
                # Set default background color if no wallpaper
                self.desktop.configure(bg='#1e1e1e')
                
        except Exception as e:
            print(f"Error setting wallpaper: {e}")
            self.desktop.configure(bg='#1e1e1e')
    
    def change_wallpaper(self, event=None):
        """Open file dialog to select a new wallpaper."""
        filetypes = [
            ('Image files', '*.png *.jpg *.jpeg *.gif *.bmp'),
            ('All files', '*.*')
        ]
        file_path = filedialog.askopenfilename(
            title="Select Wallpaper",
            filetypes=filetypes
        )
        if file_path:
            self.set_wallpaper(file_path)
    
    def save_settings(self):
        """Save desktop settings to config file."""
        config_dir = os.path.expanduser('~/.nallix')
        os.makedirs(config_dir, exist_ok=True)
        config_path = os.path.join(config_dir, 'desktop_settings.json')
        settings = {
            'wallpaper': self.wallpaper_path,
            'theme': 'dark'  # Can be expanded later
        }
        try:
            with open(config_path, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def load_settings(self):
        """Load desktop settings from config file."""
        config_path = os.path.expanduser('~/.nallix/desktop_settings.json')
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    settings = json.load(f)
                    if 'wallpaper' in settings and settings['wallpaper']:
                        self.set_wallpaper(settings['wallpaper'])
            except Exception as e:
                print(f"Error loading settings: {e}")
    
    def show_desktop_menu(self, event):
        """Show the desktop context menu."""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Change Wallpaper", command=self.change_wallpaper)
        menu.add_separator()
        menu.add_command(label="Terminal", command=self.open_terminal)
        menu.add_command(label="File Explorer", command=self.open_file_explorer)
        menu.add_separator()
        menu.add_command(label="Refresh", command=self.refresh_desktop)
        menu.add_command(label="Settings", command=self.open_settings)
        menu.add_separator()
        menu.add_command(label="Log Out", command=self.logout)
        
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
        self.root.after(1000, self.update_time)
    
    def setup_start_menu(self):
        # Start menu frame (initially hidden)
        self.start_menu = tk.Frame(
            self.root,
            bg='#1e1e1e',
            bd=1,
            relief='raised',
            width=300,
            height=400
        )
        
        # Start menu header
        header = tk.Frame(self.start_menu, bg='#0078d7', height=60)
        header.pack(fill='x')
        
        user_label = tk.Label(
            header,
            text="Nallix OS",
            bg='#0078d7',
            fg='white',
            font=('Arial', 14, 'bold'),
            anchor='w',
            padx=10
        )
        user_label.pack(side='left', fill='both', expand=True)
        
        # Start menu items
        menu_frame = tk.Frame(self.start_menu, bg='#1e1e1e')
        menu_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Add menu items
        menu_items = [
            ("Terminal", self.open_terminal),
            ("File Explorer", self.open_file_explorer),
            ("Settings", self.open_settings),
            ("Shut Down", self.shutdown)
        ]
        
        for text, command in menu_items:
            btn = tk.Button(
                menu_frame,
                text=text,
                bg='#1e1e1e',
                fg='white',
                anchor='w',
                bd=0,
                padx=10,
                command=command
            )
            btn.pack(fill='x', pady=2)
            
            # Add hover effect
            btn.bind('<Enter>', lambda e, b=btn: b.config(bg='#2d2d2d'))
            btn.bind('<Leave>', lambda e, b=btn: b.config(bg='#1e1e1e'))
    
    def toggle_start_menu(self):
        if not hasattr(self, 'start_menu_visible') or not self.start_menu_visible:
            # Show start menu
            self.start_menu.place(x=10, y=self.root.winfo_height() - 440)
            self.start_menu_visible = True
        else:
            # Hide start menu
            self.start_menu.place_forget()
            self.start_menu_visible = False
    
    def add_desktop_icons(self):
        # Get user's Nallix home directory
        nallix_home = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Home')
        current_user = os.environ.get('NALLIX_USER', 'guest')
        user_home = os.path.join(nallix_home, current_user, 'home')
        
        # Ensure user home exists
        os.makedirs(user_home, exist_ok=True)
        
        # Default system icons
        desktop_items = [
            ("Terminal", self.open_terminal, "📝"),
            ("File Explorer", self.open_file_explorer, "📁"),
            ("Settings", self.open_settings, "⚙️")
        ]
        
        # Add user files and folders
        try:
            for item in os.listdir(user_home):
                item_path = os.path.join(user_home, item)
                if os.path.isdir(item_path):
                    desktop_items.append((item, lambda x=item_path: self.open_file_explorer(x), "📁"))
                else:
                    desktop_items.append((item, lambda x=item_path: self.open_file(x), "📄"))
        except Exception as e:
            print(f"Error loading desktop items: {e}")
        
        # Display all items
        for i, (text, command, icon) in enumerate(desktop_items):
            icon_frame = tk.Frame(
                self.desktop,
                bg='#1e1e1e',
                padx=10,
                pady=5
            )
            icon_frame.grid(row=i//4, column=i%4, padx=10, pady=10, sticky='nw')
            
            # Icon
            icon_label = tk.Label(
                icon_frame,
                text=icon,
                font=('Segoe UI', 24),
                bg='#1e1e1e',
                fg='white'
            )
            icon_label.pack()
            
            # Text (truncate long names)
            display_text = text if len(text) < 15 else text[:12] + '...'
            text_label = tk.Label(
                icon_frame,
                text=display_text,
                bg='#1e1e1e',
                fg='white',
                font=('Arial', 10),
                wraplength=80
            )
            text_label.pack()
            
            # Bind click events
            for widget in (icon_label, text_label):
                widget.bind('<Button-1>', lambda e, c=command: c())
                widget.bind('<Double-Button-1>', lambda e, c=command: c())
                widget.bind('<Enter>', lambda e, f=icon_frame: f.config(bg='#2d2d2d'))
                widget.bind('<Leave>', lambda e, f=icon_frame: f.config(bg='#1e1e1e'))
            
            icon_frame.bind('<Button-1>', lambda e, c=command: c())
            icon_frame.bind('<Double-Button-1>', lambda e, c=command: c())
    
    def open_file(self, file_path):
        """Open a file with the default application"""
        try:
            if sys.platform == 'win32':
                os.startfile(file_path)
            elif sys.platform == 'darwin':  # macOS
                subprocess.run(['open', file_path])
            else:  # Linux and others
                subprocess.run(['xdg-open', file_path])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")
    
    def show_desktop_menu(self, event):
        # Create a right-click menu for the desktop
        menu = tk.Menu(self.root, tearoff=0, bg='#2d2d2d', fg='white')
        
        menu.add_command(label="New Folder", command=self.create_folder)
        menu.add_command(label="New File", command=self.create_file)
        menu.add_separator()
        menu.add_command(label="Change Wallpaper", command=self.change_wallpaper)
        menu.add_separator()
        menu.add_command(label="Refresh", command=self.refresh_desktop)
        menu.add_separator()
        menu.add_command(label="Terminal", command=self.open_terminal)
        menu.add_command(label="File Explorer", command=self.open_file_explorer)
        menu.add_separator()
        menu.add_command(label="Settings", command=self.open_settings)
        menu.add_separator()
        menu.add_command(label="Log Out", command=self.logout)
        
        menu.post(event.x_root, event.y_root)
    
    def create_folder(self):
        # Create a new folder in the user's Nallix home directory
        nallix_home = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Home')
        current_user = os.environ.get('NALLIX_USER', 'guest')
        user_home = os.path.join(nallix_home, current_user, 'home')
        
        # Ensure user home exists
        os.makedirs(user_home, exist_ok=True)
        
        folder_name = "New Folder"
        counter = 1
        
        while os.path.exists(os.path.join(user_home, folder_name)):
            folder_name = f"New Folder ({counter})"
            counter += 1
        
        try:
            os.mkdir(os.path.join(user_home, folder_name))
            self.refresh_desktop()  # Refresh to show new folder
        except Exception as e:
            messagebox.showerror("Error", f"Could not create folder: {e}")
    
    def create_file(self):
        # Create a new file in the user's Nallix home directory
        nallix_home = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Home')
        current_user = os.environ.get('NALLIX_USER', 'guest')
        user_home = os.path.join(nallix_home, current_user, 'home')
        
        # Ensure user home exists
        os.makedirs(user_home, exist_ok=True)
        
        file_name = "New File.txt"
        counter = 1
        
        while os.path.exists(os.path.join(user_home, file_name)):
            file_name = f"New File ({counter}).txt"
            counter += 1
        
        try:
            with open(os.path.join(user_home, file_name), 'w') as f:
                f.write("")
            self.refresh_desktop()  # Refresh to show new file
        except Exception as e:
            messagebox.showerror("Error", f"Could not create file: {e}")
    
    def refresh_desktop(self):
        # Refresh the desktop view
        for widget in self.desktop.winfo_children():
            widget.destroy()
        self.add_desktop_icons()
    
    def open_terminal(self):
        # Open the Nallix terminal in a new window
        try:
            term_window = tk.Toplevel(self.root)
            term_window.title("Nallix Terminal")
            term_window.geometry("800x500")
            term_window.configure(bg='#1e1e1e')
            
            # Create a frame for the terminal
            term_frame = tk.Frame(term_window, bg='#1e1e1e')
            term_frame.pack(fill='both', expand=True, padx=5, pady=5)
            
            # Add terminal title bar
            title_bar = tk.Frame(term_frame, bg='#2d2d2d', height=30)
            title_bar.pack(fill='x')
            
            title_label = tk.Label(
                title_bar,
                text="Nallix Terminal",
                bg='#2d2d2d',
                fg='white',
                font=('Arial', 10)
            )
            title_label.pack(side='left', padx=10)
            
            # Add terminal content
            terminal_text = tk.Text(
                term_frame,
                bg='#1e1e1e',
                fg='#e0e0e0',
                insertbackground='white',
                font=('Consolas', 12),
                wrap='word',
                bd=0,
                highlightthickness=0
            )
            terminal_text.pack(fill='both', expand=True, padx=5, pady=5)
            
            # Add input field at the bottom
            input_frame = tk.Frame(term_frame, bg='#2d2d2d')
            input_frame.pack(fill='x', pady=(0, 5), padx=5)
            
            prompt = tk.Label(
                input_frame,
                text="$ ",
                bg='#2d2d2d',
                fg='white',
                font=('Consolas', 12)
            )
            prompt.pack(side='left')
            
            input_entry = ttk.Entry(
                input_frame,
                font=('Consolas', 12),
                style='Terminal.TEntry'
            )
            input_entry.pack(fill='x', expand=True, padx=5)
            input_entry.focus()
            
            def execute_command(event=None):
                command = input_entry.get()
                if not command.strip():
                    return
                    
                # Display command
                terminal_text.config(state='normal')
                terminal_text.insert('end', f"$ {command}\n")
                
                try:
                    # Handle special commands
                    if command.lower() in ('exit', 'quit'):
                        term_window.destroy()
                        return
                    elif command.lower() == 'clear':
                        terminal_text.delete('1.0', 'end')
                        input_entry.delete(0, 'end')
                        return
                    elif command.lower() == 'kex':
                        # Launch desktop GUI
                        terminal_text.insert('end', "Already in Nallix Desktop environment.\n")
                        input_entry.delete(0, 'end')
                        terminal_text.see('end')
                        return
                    elif command.lower() == 'help':
                        help_text = """Nallix Terminal - Available commands:
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
  log out           - Sign out current user and switch to guest
"""
                        terminal_text.insert('end', help_text)
                        input_entry.delete(0, 'end')
                        terminal_text.see('end')
                        return
                    
                    # Handle Nallix commands
                    if command.startswith('cd '):
                        try:
                            target = command[3:].strip('"\'')
                            os.chdir(target)
                            result = os.getcwd()
                        except Exception as e:
                            result = f"cd: {str(e)}"
                    else:
                        # Try to run as Nallix command first
                        try:
                            # Import Nallix terminal functions
                            from Terminal import run_command
                            result = run_command(command)
                            if result is None:
                                result = ""
                        except Exception as e:
                            # Fall back to system command if not a Nallix command
                            try:
                                result = subprocess.getoutput(command)
                            except Exception as e:
                                result = f"Command error: {str(e)}"
                    
                    # Display result if not empty
                    if result:
                        terminal_text.insert('end', f"{result}\n")
                except Exception as e:
                    terminal_text.insert('end', f"Error: {str(e)}\n")
                
                # Clear input and scroll to bottom
                input_entry.delete(0, 'end')
                terminal_text.see('end')
                terminal_text.config(state='disabled')
            
            # Bind Enter key to execute command
            input_entry.bind('<Return>', execute_command)
            
            # Make terminal text read-only
            terminal_text.config(state='disabled')
            
        except Exception as e:
            messagebox.showerror("Error", f"Could not open terminal: {e}")
    
    def open_file_explorer(self):
        # Open the file explorer
        try:
            if sys.platform == 'win32':
                os.startfile(os.path.expanduser('~'))
            else:
                subprocess.Popen(['xdg-open', os.path.expanduser('~')])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file explorer: {e}")
    
    def open_settings(self):
        # Open settings dialog
        settings = tk.Toplevel(self.root)
        settings.title("System Settings")
        settings.geometry("700x500")
        settings.configure(bg='#2d2d2d')
        
        # Create notebook for settings tabs
        notebook = ttk.Notebook(settings)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # System Info Tab
        sys_info_frame = ttk.Frame(notebook, padding=10)
        notebook.add(sys_info_frame, text='System Info')
        
        # Get system information
        sys_info = {
            "OS": f"{platform.system()} {platform.release()}",
            "Version": platform.version(),
            "Machine": platform.machine(),
            "Processor": platform.processor(),
            "Hostname": socket.gethostname(),
            "IP Address": socket.gethostbyname(socket.gethostname()),
            "CPU Cores": psutil.cpu_count(logical=True),
            "Total RAM": f"{psutil.virtual_memory().total / (1024**3):.2f} GB"
        }
        
        # Display system information
        for i, (key, value) in enumerate(sys_info.items()):
            tk.Label(
                sys_info_frame,
                text=f"{key}:",
                font=('Arial', 10, 'bold'),
                bg='#2d2d2d',
                fg='white'
            ).grid(row=i, column=0, sticky='w', pady=2, padx=5)
            
            tk.Label(
                sys_info_frame,
                text=value,
                bg='#2d2d2d',
                fg='#a0a0a0'
            ).grid(row=i, column=1, sticky='w', pady=2)
        
        # Appearance Tab
        appearance_frame = ttk.Frame(notebook, padding=10)
        notebook.add(appearance_frame, text='Appearance')
        
        # Theme selection
        tk.Label(
            appearance_frame,
            text="Theme:",
            font=('Arial', 10, 'bold'),
            bg='#2d2d2d',
            fg='white'
        ).pack(anchor='w', pady=(10, 5))
        
        theme_var = tk.StringVar(value='dark')
        themes = [('Dark', 'dark'), ('Light', 'light'), ('Blue', 'blue')]
        
        for text, mode in themes:
            rb = ttk.Radiobutton(
                appearance_frame,
                text=text,
                variable=theme_var,
                value=mode
            )
            rb.pack(anchor='w')
        
        # Terminal Settings Tab
        terminal_frame = ttk.Frame(notebook, padding=10)
        notebook.add(terminal_frame, text='Terminal')
        
        # Font size
        tk.Label(
            terminal_frame,
            text="Font Size:",
            font=('Arial', 10, 'bold'),
            bg='#2d2d2d',
            fg='white'
        ).pack(anchor='w', pady=(10, 5))
        
        font_size = tk.Scale(
            terminal_frame,
            from_=8,
            to=24,
            orient='horizontal',
            length=200
        )
        font_size.set(12)
        font_size.pack(anchor='w')
        
        # Save button
        save_btn = ttk.Button(
            settings,
            text="Save Settings",
            command=lambda: self.save_settings({
                'theme': theme_var.get(),
                'font_size': font_size.get()
            }, settings)
        )
        save_btn.pack(pady=10)
    
    def save_settings(self, settings, window):
        # Save settings to a config file
        config_path = os.path.join(os.path.expanduser('~'), '.nallix_config.json')
        try:
            with open(config_path, 'w') as f:
                json.dump(settings, f)
            messagebox.showinfo("Success", "Settings saved successfully!")
            window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save settings: {e}")
    
    def logout(self):
        # Log out the current user and return to login
        if messagebox.askyesno("Log Out", "Are you sure you want to log out?"):
            from Terminal import clear_session
            clear_session()
            self.root.destroy()
            
            # Restart the desktop as guest
            python = sys.executable
            os.execl(python, python, *sys.argv)
    
    def shutdown(self):
        # Show shutdown confirmation
        if messagebox.askyesno("Shut Down", "Are you sure you want to shut down?"):
            self.root.destroy()

def main():
    root = tk.Tk()
    
    # Set environment variable to indicate we're in desktop mode
    os.environ['NALLIX_DESKTOP'] = '1'
    
    # Set window icon if available
    try:
        root.iconbitmap(os.path.join(os.path.dirname(__file__), 'nallix.ico'))
    except:
        pass

    # Create and run the desktop
    desktop = DesktopApp(root)
    # Hide the main window initially if launched from terminal
    if 'NALLIX_TERMINAL_LAUNCH' in os.environ:
        root.withdraw()

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()
