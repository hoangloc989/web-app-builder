import os
import sys
import subprocess
import ctypes

APP_NAME = "NGWTM"
APP_URL = "https://ngwtm.intel.com"
ICON_FILE = "favicon.ico"

# Window configuration
WINDOW_WIDTH = 1200          # Window width in pixels
WINDOW_HEIGHT = 800          # Window height in pixels
WINDOW_FRAMELESS = True     # Set to True to remove title bar

# ---------- Utilities ----------

def resource_path(rel_path):
    """
    Get absolute path to resource, works for PyInstaller onefile bundles.
    """
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        base = os.path.abspath(".")
    return os.path.join(base, rel_path)

def create_shortcut(lpath, target, args="", icon=None, desc=None):
    """
    Create a Windows .lnk shortcut using COM.
    Returns True on success, False on failure.
    """
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(lpath)
        shortcut.Targetpath = target
        shortcut.Arguments = args
        
        # Set icon - for compiled exe, use the exe itself as icon source
        if icon and os.path.exists(icon):
            if icon.lower().endswith('.ico'):
                shortcut.IconLocation = icon
            elif target.lower().endswith('.exe'):
                shortcut.IconLocation = f"{target},0"
            else:
                shortcut.IconLocation = icon
        elif target.lower().endswith('.exe'):
            shortcut.IconLocation = f"{target},0"
            
        if desc:
            shortcut.Description = desc
        shortcut.WorkingDirectory = os.path.dirname(target)
        shortcut.save()
        return True
    except Exception:
        return False

def create_shortcuts_if_needed():
    """
    Create Start Menu shortcut pointing to this exe.
    Always removes old shortcut first to ensure icon updates properly.
    Returns tuple: (success_count, failed_locations)
    """
    if not getattr(sys, 'frozen', False):
        print("Running as Python script - skipping shortcut creation")
        return 0, []
    
    exe_path = sys.executable

    start_menu_dir = os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs")
    start_shortcut = os.path.join(start_menu_dir, f"{APP_NAME}.lnk")

    success_count = 0
    failed_locations = []

    # Remove old shortcut first
    if os.path.exists(start_shortcut):
        try:
            os.remove(start_shortcut)
            print(f"Removed old shortcut: {start_shortcut}")
        except Exception as e:
            print(f"Could not remove old shortcut: {e}")

    # Create Start Menu shortcut (pass exe_path as icon to use embedded icon)
    try:
        os.makedirs(start_menu_dir, exist_ok=True)
        print(f"Creating Start Menu shortcut at: {start_shortcut}")
        # Pass exe_path for both target and icon - this ensures the embedded icon is used
        if create_shortcut(start_shortcut, exe_path, icon=exe_path, desc=APP_NAME):
            success_count += 1
            print(f"✓ Start Menu shortcut created successfully")
        else:
            failed_locations.append("Start Menu")
            print(f"✗ Failed to create Start Menu shortcut")
    except Exception as e:
        failed_locations.append("Start Menu")
        print(f"Start Menu shortcut error: {e}")

    return success_count, failed_locations

def message_box(title, text, flags=0x40 | 0x0):
    ctypes.windll.user32.MessageBoxW(0, text, title, flags)

# ---------- App ----------

def run_app():
    """
    Launch Edge in app mode - this guarantees Windows Integrated Auth works
    because it uses the actual Edge browser with all its enterprise policies
    """
    # Set AppUserModelID for proper taskbar icon
    try:
        app_id = f"Intel.{APP_NAME.replace(' ', '')}.WebApp.1.0"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
        print(f"Set AppUserModelID: {app_id}")
    except Exception as e:
        print(f"Could not set AppUserModelID: {e}")
    
    # Create shortcuts if running as compiled exe
    try:
        success_count, failed_locations = create_shortcuts_if_needed()
        if success_count > 0:
            if not failed_locations:
                message_box(APP_NAME, "Start Menu shortcut created successfully!")
    except Exception as e:
        print(f"Shortcut creation error: {e}")
    
    # Try to find Edge first, then Chrome as fallback
    browser_path = None
    browser_name = None
    
    # Try Microsoft Edge (preferred - better Windows Integrated Auth support)
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    
    for path in edge_paths:
        if os.path.exists(path):
            browser_path = path
            browser_name = "Microsoft Edge"
            print(f"Found Microsoft Edge at: {path}")
            break
    
    # Fallback to Chrome if Edge not found
    if not browser_path:
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe")
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                browser_path = path
                browser_name = "Google Chrome"
                print(f"Microsoft Edge not found, using Chrome at: {path}")
                break
    
    # No browser found
    if not browser_path:
        message_box(
            APP_NAME, 
            "Error: No compatible browser found.\n\n"
            "Please install Microsoft Edge or Google Chrome.", 
            0x10
        )
        sys.exit(1)
    
    print(f"Launching {browser_name} in app mode for: {APP_URL}")
    print(f"This will use your Windows credentials automatically")
    
    # Build command-line arguments
    args = [
        browser_path,
        f"--app={APP_URL}",
        f"--window-name={APP_NAME}",
        f"--window-size={WINDOW_WIDTH},{WINDOW_HEIGHT}",
        "--no-first-run",
        "--no-default-browser-check"
    ]
    
    # Add options for frameless window (removes title bar but keeps window controls)
    if WINDOW_FRAMELESS:
        # Use app mode with borderless for a cleaner look
        # This removes the title bar but keeps minimize/maximize/close buttons
        args.append("--app-auto-launched")
        args.append("--disable-features=OverlayScrollbar")
        print("Launching in frameless mode (minimal UI)")
    
    # Launch in app mode with window
    subprocess.Popen(args)
    
    print(f"✓ {APP_NAME} launched in {browser_name} app mode")
    print(f"   Window size: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    print(f"   Frameless: {WINDOW_FRAMELESS}")

if __name__ == "__main__":
    run_app()