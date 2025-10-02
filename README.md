# Web App Builder

**Version:** 1.0.0  
**Owner:** OMT Data MLG

A Windows desktop application that converts web applications into standalone executable launchers with Windows Integrated Authentication (SSO) support.

## 🎯 Overview

Web App Builder allows you to create custom desktop launchers for web applications without writing any code. Simply fill in a form, and it generates a standalone `.exe` file that opens your web application in a frameless browser window with full Windows SSO support.

## ✨ Features

- **🖱️ Simple GUI Interface** - No coding required, just fill in the form
- **🔐 Windows Integrated Authentication** - Automatic SSO with Intel/corporate web apps
- **🎨 Custom Icons** - Use your own `.ico` file or the default icon
- **📏 Configurable Window Size** - Set custom width and height
- **🪟 Frameless Mode** - Optional borderless window (no title bar)
- **📌 Start Menu Shortcuts** - Automatically create Start Menu shortcuts
- **🧹 Clean Output** - Only `.exe` and `.log` files in output folder
- **🌐 Browser Fallback** - Uses Microsoft Edge or Google Chrome
- **📦 Single File Output** - Each app is a single standalone executable

## 📋 Prerequisites

### For Running the App Builder (Script Mode)
- **Python 3.7+** installed
- **PyInstaller** - Install with: `pip install pyinstaller`
- **pywin32** - Install with: `pip install pywin32`

### For Using the App Builder (Exe Mode)
- **Windows 10/11**
- **Microsoft Edge** or **Google Chrome** installed
- No other dependencies needed!

## 🚀 Quick Start

### Method 1: Run from Source
```cmd
python app_builder.py
```

### Method 2: Build and Run as Exe
```cmd
build_app_builder.bat
```
Then run `dist\Web App Builder.exe`

## 📖 User Guide

### Creating a Web App Launcher

1. **Launch Web App Builder**
   - Run `Web App Builder.exe` or `python app_builder.py`

2. **Fill in the Form**
   - **App Name**: Enter a friendly name (e.g., "PerformX", "MFG Store")
     - Spaces are allowed in the name
   - **Web URL**: Enter the full URL (must start with `http://` or `https://`)
     - Example: `https://performx.intel.com`
   - **Icon File**: (Optional) Browse and select a `.ico` file
     - If left empty, uses the default icon
   - **Window Size**: Set width and height in pixels
     - Default: 1200 × 800
     - Minimum: 100 × 100
   - **Options**:
     - ☑️ Create Start Menu shortcut (recommended)
     - ☐ Frameless window (removes title bar)

3. **Click "Create App"**
   - PyInstaller will build the executable
   - Progress bar shows build status
   - Success message displays when complete

4. **Find Your App**
   - Click "Open Output Folder" button
   - Or navigate to: `output\{AppName}\dist\{AppName}.exe`

### Example Use Cases

#### Intel PerformX Application
```
App Name: PerformX
Web URL: https://performx.intel.com
Icon File: (leave empty for default)
Window Size: 1200 × 800
☑️ Create Start Menu shortcut
☐ Frameless window
```

#### Intel MFG Store
```
App Name: MFG Store
Web URL: https://mfgstore.intel.com
Icon File: (browse to custom icon)
Window Size: 1400 × 900
☑️ Create Start Menu shortcut
☑️ Frameless window
```

## 🏗️ Building the App Builder

To create a distributable `Web App Builder.exe`:

### Using the Batch Script (Recommended)
```cmd
build_app_builder.bat
```

### Manual Build Command
```cmd
pyinstaller --onefile --windowed ^
    --name="Web App Builder" ^
    --icon=app_icon.ico ^
    --add-data="app_icon.ico;." ^
    --clean ^
    app_builder.py
```

### Output Location
The executable will be created at: `dist\Web App Builder.exe`

## 📁 Project Structure

```
performx-app/
├── app_builder.py              # Main application source code
├── app_icon.ico                # Default icon (bundled in exe)
├── build_app_builder.bat       # Build script for App Builder
├── BUILD_INSTRUCTIONS.md       # Detailed build instructions
├── SOLUTION_SUMMARY.md         # Technical documentation
├── README.md                   # This file
├── main_edge.py                # (Legacy) Template for launchers
└── output/                     # Generated apps output folder
    └── {AppName}/
        └── dist/
            └── {AppName}.exe   # Your generated app!
```

## 🔧 How It Works

### The Generated Apps

Each app created by Web App Builder:

1. **Searches for Browser**
   - Tries Microsoft Edge (preferred)
   - Falls back to Google Chrome
   - Shows error if neither found

2. **Launches in App Mode**
   - Uses `--app={URL}` flag for frameless browser
   - Sets custom window size
   - Enables Windows Integrated Authentication
   - No address bar or browser UI

3. **Creates Shortcuts** (if enabled)
   - Start Menu: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\`
   - Uses embedded exe icon
   - Shows proper name in Start Menu

4. **Windows SSO Integration**
   - Automatically inherits enterprise authentication
   - No login prompts for internal Intel sites
   - Uses Kerberos/NTLM as configured in Windows

## 🎨 Customization

### Changing Default Icon
Replace `app_icon.ico` with your own icon file (must be `.ico` format)

### Adjusting Default Values
Edit `app_builder.py`:
```python
self.app_name = tk.StringVar(value="My Web App")
self.app_url = tk.StringVar(value="https://example.com")
self.window_width = tk.StringVar(value="1200")
self.window_height = tk.StringVar(value="800")
```

### Updating Version
Edit `app_builder.py`:
```python
class WebAppBuilder:
    VERSION = "1.0.0"
    OWNER = "OMT Data MLG"
```

## 🐛 Troubleshooting

### "Please select an icon file or ensure app_icon.ico exists"
**Solution:** Make sure `app_icon.ico` is in the same directory as `app_builder.py` or the exe.

### "PyInstaller failed"
**Solution:** 
- Ensure PyInstaller is installed: `pip install pyinstaller`
- Check that `pywin32` is installed: `pip install pywin32`
- Try running as administrator

### "No compatible browser found"
**Solution:** Install Microsoft Edge or Google Chrome on the target machine.

### Generated app requires login despite SSO
**Cause:** The browser's app mode inherits Windows authentication automatically.
**Solution:** 
- Ensure the user is logged into Windows with their corporate account
- Check that the website URL is in the Trusted Sites or Intranet zone
- Verify that Windows Integrated Authentication is enabled in browser settings

### Start Menu shortcut not created
**Solution:** 
- Run the generated app once to create the shortcut
- Check permissions for: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\`
- Try running the app as administrator once

## 📝 Technical Details

### Technologies Used
- **Python 3.x** - Application runtime
- **tkinter** - GUI framework (built into Python)
- **PyInstaller** - Converts Python scripts to executables
- **Microsoft Edge / Chrome** - Browser engine with `--app` mode
- **pywin32** - Windows COM automation for shortcuts

### Browser Arguments
```python
--app={URL}                      # App mode (no browser UI)
--window-name={APP_NAME}         # Window title
--window-size={WIDTH},{HEIGHT}   # Initial size
--no-first-run                   # Skip first-run prompts
--no-default-browser-check       # Skip default browser check
--app-auto-launched              # (frameless mode)
--disable-features=OverlayScrollbar  # (frameless mode)
```

### File Cleanup
After building, these files are automatically removed:
- `build/` directory
- `.spec` files
- `app_launcher.py` (generated script)
- `app_icon.ico` (temporary copy)
- All non-exe/log files in `dist/`

## 🔒 Security Considerations

- ✅ Uses official Microsoft Edge or Google Chrome browsers
- ✅ Inherits Windows security policies and authentication
- ✅ No embedded web engine or custom security implementation
- ✅ Respects corporate proxy and network settings
- ✅ SSL/TLS handled by the browser
- ⚠️ Apps open specific URLs only - users cannot navigate elsewhere

## 📄 License

Internal tool for OMT Data MLG use.

## 🎉 Acknowledgments

Created by OMT Data MLG team to simplify web application deployment and improve user experience with Windows Integrated Authentication.

---

**Version History**

- **v1.0.0** (October 2025)
  - Initial release
  - White background UI
  - Default icon support
  - Automatic output cleanup
  - Version and owner display
  - Window icon integration
