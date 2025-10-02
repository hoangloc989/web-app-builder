import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import sys
import subprocess
import shutil
import threading

# Try to import PIL for PNG to ICO conversion
try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

class WebAppBuilder:
    VERSION = "1.0.0"
    OWNER = "OMT Data MLG"
    
    def __init__(self, root):
        self.root = root
        self.root.title("Web App Builder")
        self.root.geometry("650x580")
        self.root.resizable(False, False)  # Disable window resizing
        self.root.configure(bg='white')  # Set white background
        
        # Set default icon path
        self.default_icon_path = self.get_bundled_icon_path()
        
        # Set window icon
        if os.path.exists(self.default_icon_path):
            try:
                self.root.iconbitmap(self.default_icon_path)
            except Exception:
                pass  # Icon setting failed, continue without it
        
        # Variables
        self.app_name = tk.StringVar(value="My Web App")
        self.app_url = tk.StringVar(value="https://example.com")
        self.icon_path = tk.StringVar(value="")
        self.window_width = tk.StringVar(value="1200")
        self.window_height = tk.StringVar(value="800")
        self.create_shortcut = tk.BooleanVar(value=True)
        self.frameless = tk.BooleanVar(value=False)
        
        self.create_ui()
    
    def get_bundled_icon_path(self):
        """Get path to bundled default icon, works for both dev and PyInstaller exe"""
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller exe
            base_path = sys._MEIPASS
        else:
            # Running as script
            base_path = os.path.dirname(os.path.abspath(__file__))
        
        return os.path.join(base_path, "app_icon.ico")
    
    def create_ui(self):
        # Configure style for white background
        style = ttk.Style()
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white')
        style.configure('TCheckbutton', background='white')
        style.configure('TLabelframe', background='white')
        style.configure('TLabelframe.Label', background='white')
        
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure column weights to make everything expand
        main_frame.columnconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Web App Builder", font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 5))
        
        # Version and Owner info
        info_label = ttk.Label(main_frame, text=f"v{self.VERSION} | {self.OWNER}", font=('Arial', 9), foreground='gray')
        info_label.grid(row=1, column=0, columnspan=3, pady=(0, 15))
        
        # App Name
        ttk.Label(main_frame, text="App Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.app_name).grid(row=2, column=1, columnspan=2, pady=5, sticky=(tk.W, tk.E), padx=(5, 0))
        ttk.Label(main_frame, text="(Can contain spaces)", font=('Arial', 8), foreground='gray').grid(row=3, column=1, columnspan=2, sticky=tk.W, padx=(5, 0))
        
        # Web URL
        ttk.Label(main_frame, text="Web URL:").grid(row=4, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.app_url).grid(row=4, column=1, columnspan=2, pady=5, sticky=(tk.W, tk.E), padx=(5, 0))
        
        # Icon File
        icon_label_text = "Icon File (.ico/.png):" if PIL_AVAILABLE else "Icon File (.ico):"
        ttk.Label(main_frame, text=icon_label_text).grid(row=5, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.icon_path).grid(row=5, column=1, pady=5, sticky=(tk.W, tk.E), padx=(5, 5))
        ttk.Button(main_frame, text="Browse...", command=self.browse_icon).grid(row=5, column=2, pady=5, sticky=tk.E)
        
        hint_text = "(Optional - uses default icon if not specified. PNG will be converted to ICO)" if PIL_AVAILABLE else "(Optional - uses default icon if not specified)"
        ttk.Label(main_frame, text=hint_text, font=('Arial', 8), foreground='gray').grid(row=6, column=1, columnspan=2, sticky=tk.W, padx=(5, 0))
        
        # Window Size
        size_frame = ttk.LabelFrame(main_frame, text="Window Size", padding="10")
        size_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        size_frame.columnconfigure(1, weight=1)
        size_frame.columnconfigure(3, weight=1)
        
        ttk.Label(size_frame, text="Width:").grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        ttk.Entry(size_frame, textvariable=self.window_width, width=10).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Label(size_frame, text="Height:").grid(row=0, column=2, sticky=tk.W, padx=(10, 5))
        ttk.Entry(size_frame, textvariable=self.window_height, width=10).grid(row=0, column=3, sticky=(tk.W, tk.E))
        
        # Options
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="10")
        options_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Checkbutton(options_frame, text="Create Start Menu shortcut", variable=self.create_shortcut).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(options_frame, text="Frameless window (no title bar)", variable=self.frameless).grid(row=1, column=0, sticky=tk.W)
        
        # Progress/Status
        self.status_label = ttk.Label(main_frame, text="Ready to build", foreground='gray')
        self.status_label.grid(row=9, column=0, columnspan=3, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=10, column=0, columnspan=3, pady=5, sticky=(tk.W, tk.E))
        
        # Build Button
        self.build_button = ttk.Button(main_frame, text="Create App", command=self.build_app)
        self.build_button.grid(row=11, column=0, columnspan=3, pady=20, sticky=(tk.W, tk.E))
        
        # Output folder button
        self.output_button = ttk.Button(main_frame, text="Open Output Folder", command=self.open_output_folder, state='disabled')
        self.output_button.grid(row=12, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
    def browse_icon(self):
        filetypes = [("Icon Files", "*.ico")]
        if PIL_AVAILABLE:
            filetypes.insert(0, ("Image Files", "*.ico *.png"))
            filetypes.append(("PNG Files", "*.png"))
        filetypes.append(("All Files", "*.*"))
        
        filename = filedialog.askopenfilename(
            title="Select Icon File",
            filetypes=filetypes
        )
        if filename:
            self.icon_path.set(filename)
    
    def validate_inputs(self):
        if not self.app_name.get().strip():
            messagebox.showerror("Error", "Please enter an app name")
            return False
        
        if not self.app_url.get().strip():
            messagebox.showerror("Error", "Please enter a web URL")
            return False
        
        if not self.app_url.get().startswith(('http://', 'https://')):
            messagebox.showerror("Error", "URL must start with http:// or https://")
            return False
        
        # If no icon specified, use default app_icon.ico
        if not self.icon_path.get():
            if os.path.exists(self.default_icon_path):
                self.icon_path.set(self.default_icon_path)
            else:
                messagebox.showerror("Error", "Please select an icon file or ensure app_icon.ico exists")
                return False
        
        if not os.path.exists(self.icon_path.get()):
            messagebox.showerror("Error", "Icon file not found")
            return False
        
        # Check if it's a PNG file and PIL is not available
        if self.icon_path.get().lower().endswith('.png') and not PIL_AVAILABLE:
            messagebox.showerror(
                "Error", 
                "PNG support requires Pillow library.\n\n"
                "Install with: pip install Pillow\n\n"
                "Or use an .ico file instead."
            )
            return False
        
        try:
            width = int(self.window_width.get())
            height = int(self.window_height.get())
            if width < 100 or height < 100:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Error", "Window size must be valid numbers (min 100x100)")
            return False
        
        return True
    
    def convert_png_to_ico(self, png_path, ico_path):
        """Convert PNG file to ICO format with multiple sizes"""
        try:
            img = Image.open(png_path)
            
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Create icon with multiple sizes for better quality
            icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
            
            # Resize image to all sizes
            img.save(ico_path, format='ICO', sizes=icon_sizes)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert PNG to ICO:\n{str(e)}")
            return False
    
    def get_safe_filename(self, name):
        """Convert app name to safe filename (no spaces, special chars)"""
        # Remove or replace special characters
        safe_name = "".join(c if c.isalnum() or c in (' ', '-', '_') else '' for c in name)
        # Replace spaces with underscores
        safe_name = safe_name.replace(' ', '_')
        # Remove multiple underscores
        while '__' in safe_name:
            safe_name = safe_name.replace('__', '_')
        return safe_name.strip('_')
    
    def generate_main_script(self, output_dir):
        """Generate the main_edge.py script with user's settings"""
        app_name = self.app_name.get().strip()
        app_url = self.app_url.get().strip()
        width = self.window_width.get()
        height = self.window_height.get()
        frameless = str(self.frameless.get())
        create_shortcut = self.create_shortcut.get()
        
        script_content = f'''import os
import sys
import subprocess
import ctypes

APP_NAME = "{app_name}"
APP_URL = "{app_url}"
ICON_FILE = "app_icon.ico"

# Window configuration
WINDOW_WIDTH = {width}
WINDOW_HEIGHT = {height}
WINDOW_FRAMELESS = {frameless}
CREATE_SHORTCUT = {create_shortcut}

# ---------- Utilities ----------

def resource_path(rel_path):
    """Get absolute path to resource, works for PyInstaller onefile bundles."""
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.abspath(".")
    return os.path.join(base, rel_path)

def create_shortcut(lpath, target, args="", icon=None, desc=None):
    """Create a Windows .lnk shortcut using COM."""
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(lpath)
        shortcut.Targetpath = target
        shortcut.Arguments = args
        
        if icon and os.path.exists(icon):
            if icon.lower().endswith('.ico'):
                shortcut.IconLocation = icon
            elif target.lower().endswith('.exe'):
                shortcut.IconLocation = f"{{target}},0"
            else:
                shortcut.IconLocation = icon
        elif target.lower().endswith('.exe'):
            shortcut.IconLocation = f"{{target}},0"
            
        if desc:
            shortcut.Description = desc
        shortcut.WorkingDirectory = os.path.dirname(target)
        shortcut.save()
        return True
    except Exception:
        return False

def create_shortcuts_if_needed():
    """Create Start Menu shortcut pointing to this exe."""
    if not CREATE_SHORTCUT:
        return 0, []
        
    if not getattr(sys, 'frozen', False):
        return 0, []
    
    exe_path = sys.executable
    start_menu_dir = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\\Windows\\Start Menu\\Programs")
    start_shortcut = os.path.join(start_menu_dir, f"{{APP_NAME}}.lnk")

    success_count = 0
    failed_locations = []

    # Remove old shortcut first
    if os.path.exists(start_shortcut):
        try:
            os.remove(start_shortcut)
        except Exception:
            pass

    # Create Start Menu shortcut
    try:
        os.makedirs(start_menu_dir, exist_ok=True)
        if create_shortcut(start_shortcut, exe_path, icon=exe_path, desc=APP_NAME):
            success_count += 1
        else:
            failed_locations.append("Start Menu")
    except Exception:
        failed_locations.append("Start Menu")

    return success_count, failed_locations

def message_box(title, text, flags=0x40 | 0x0):
    ctypes.windll.user32.MessageBoxW(0, text, title, flags)

# ---------- App ----------

def run_app():
    """Launch browser in app mode."""
    # Set AppUserModelID for proper taskbar icon
    try:
        app_id = f"WebApp.{{APP_NAME.replace(' ', '')}}.1.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    except Exception:
        pass
    
    # Create shortcuts if enabled
    if CREATE_SHORTCUT:
        try:
            success_count, failed_locations = create_shortcuts_if_needed()
            if success_count > 0 and not failed_locations:
                message_box(APP_NAME, "Start Menu shortcut created successfully!")
        except Exception:
            pass
    
    # Try to find Edge first, then Chrome as fallback
    browser_path = None
    browser_name = None
    
    # Try Microsoft Edge
    edge_paths = [
        r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        r"C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe"
    ]
    
    for path in edge_paths:
        if os.path.exists(path):
            browser_path = path
            browser_name = "Microsoft Edge"
            break
    
    # Fallback to Chrome
    if not browser_path:
        chrome_paths = [
            r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
            r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\\Google\\Chrome\\Application\\chrome.exe")
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                browser_path = path
                browser_name = "Google Chrome"
                break
    
    # No browser found
    if not browser_path:
        message_box(
            APP_NAME, 
            "Error: No compatible browser found.\\n\\n"
            "Please install Microsoft Edge or Google Chrome.", 
            0x10
        )
        sys.exit(1)
    
    # Build command-line arguments
    args = [
        browser_path,
        f"--app={{APP_URL}}",
        f"--window-name={{APP_NAME}}",
        f"--window-size={{WINDOW_WIDTH}},{{WINDOW_HEIGHT}}",
        "--no-first-run",
        "--no-default-browser-check"
    ]
    
    # Add options for frameless window
    if WINDOW_FRAMELESS:
        args.append("--app-auto-launched")
        args.append("--disable-features=OverlayScrollbar")
    
    # Launch browser
    subprocess.Popen(args)

if __name__ == "__main__":
    run_app()
'''
        
        script_path = os.path.join(output_dir, "app_launcher.py")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        return script_path
    
    def build_app(self):
        if not self.validate_inputs():
            return
        
        # Disable button and start progress
        self.build_button.config(state='disabled')
        self.output_button.config(state='disabled')
        self.progress.start()
        self.status_label.config(text="Building app...", foreground='blue')
        
        # Run build in separate thread
        thread = threading.Thread(target=self.build_thread)
        thread.daemon = True
        thread.start()
    
    def build_thread(self):
        try:
            app_name = self.app_name.get().strip()
            safe_name = self.get_safe_filename(app_name)
            
            # Create output directory
            output_dir = os.path.join(os.getcwd(), "output", safe_name)
            os.makedirs(output_dir, exist_ok=True)
            
            # Handle icon file - convert PNG to ICO if needed
            icon_dest = os.path.join(output_dir, "app_icon.ico")
            icon_source = self.icon_path.get()
            
            if icon_source.lower().endswith('.png'):
                # Convert PNG to ICO
                self.update_status("Converting PNG to ICO...")
                if not self.convert_png_to_ico(icon_source, icon_dest):
                    self.root.after(0, lambda: self.build_error("Failed to convert PNG to ICO"))
                    return
            else:
                # Just copy ICO file
                shutil.copy2(icon_source, icon_dest)
            
            # Generate main script
            script_path = self.generate_main_script(output_dir)
            
            # Build with PyInstaller
            self.update_status("Running PyInstaller...")
            
            cmd = [
                "pyinstaller",
                "--onefile",
                "--windowed",
                f"--name={app_name}",
                f"--icon={icon_dest}",
                f"--add-data={icon_dest};.",
                "--clean",
                script_path
            ]
            
            # Hide console window on Windows
            startupinfo = None
            if sys.platform == 'win32':
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
            
            result = subprocess.run(
                cmd,
                cwd=output_dir,
                capture_output=True,
                text=True,
                startupinfo=startupinfo
            )
            
            if result.returncode == 0:
                # Success!
                exe_path = os.path.join(output_dir, "dist", f"{app_name}.exe")
                if os.path.exists(exe_path):
                    # Clean up output folder - keep only exe and log files
                    self.cleanup_output_folder(output_dir)
                    
                    self.output_dir = os.path.join(output_dir, "dist")
                    self.root.after(0, self.build_success)
                else:
                    self.root.after(0, lambda: self.build_error("Executable not found after build"))
            else:
                self.root.after(0, lambda: self.build_error(f"PyInstaller failed: {result.stderr[:200]}"))
                
        except Exception as e:
            self.root.after(0, lambda: self.build_error(str(e)))
    
    def cleanup_output_folder(self, output_dir):
        """Remove everything except exe and log files from output folder"""
        try:
            dist_dir = os.path.join(output_dir, "dist")
            build_dir = os.path.join(output_dir, "build")
            
            # Remove build directory entirely
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
            
            # Remove .spec file
            for file in os.listdir(output_dir):
                if file.endswith('.spec'):
                    os.remove(os.path.join(output_dir, file))
            
            # Remove app_launcher.py and app_icon.ico from root output dir
            launcher_path = os.path.join(output_dir, "app_launcher.py")
            if os.path.exists(launcher_path):
                os.remove(launcher_path)
            
            icon_path = os.path.join(output_dir, "app_icon.ico")
            if os.path.exists(icon_path):
                os.remove(icon_path)
            
            # In dist folder, keep only .exe and .log files
            if os.path.exists(dist_dir):
                for file in os.listdir(dist_dir):
                    file_path = os.path.join(dist_dir, file)
                    if os.path.isfile(file_path):
                        # Keep only exe and log files
                        if not (file.endswith('.exe') or file.endswith('.log')):
                            os.remove(file_path)
                    elif os.path.isdir(file_path):
                        # Remove any subdirectories
                        shutil.rmtree(file_path)
        except Exception as e:
            print(f"Warning: Could not fully clean output folder: {e}")
    
    def update_status(self, message):
        self.root.after(0, lambda: self.status_label.config(text=message))
    
    def build_success(self):
        self.progress.stop()
        self.status_label.config(text="✓ App created successfully!", foreground='green')
        self.build_button.config(state='normal')
        self.output_button.config(state='normal')
        
        messagebox.showinfo(
            "Success",
            f"App '{self.app_name.get()}' created successfully!\n\n"
            f"Location: {self.output_dir}\n\n"
            "Click 'Open Output Folder' to view the executable."
        )
    
    def build_error(self, error_msg):
        self.progress.stop()
        self.status_label.config(text="✗ Build failed", foreground='red')
        self.build_button.config(state='normal')
        messagebox.showerror("Build Error", f"Failed to build app:\n\n{error_msg}")
    
    def open_output_folder(self):
        if hasattr(self, 'output_dir') and os.path.exists(self.output_dir):
            os.startfile(self.output_dir)
        else:
            messagebox.showwarning("Warning", "Output folder not found")

def main():
    root = tk.Tk()
    app = WebAppBuilder(root)
    root.mainloop()

if __name__ == "__main__":
    main()
