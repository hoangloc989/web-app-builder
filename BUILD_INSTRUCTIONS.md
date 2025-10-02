# Building Web App Builder

## Prerequisites
1. Python 3.x installed
2. PyInstaller installed: `pip install pyinstaller`
3. `app_icon.ico` file in the same directory as `app_builder.py`

## Build Methods

### Method 1: Using the Batch Script (Easiest)
Simply double-click `build_app_builder.bat` or run:
```cmd
build_app_builder.bat
```

### Method 2: Manual PyInstaller Command
Run this command in the terminal:
```cmd
pyinstaller --onefile --windowed --name="Web App Builder" --icon=app_icon.ico --add-data="app_icon.ico;." --clean app_builder.py
```

## Output
The executable will be created at: `dist\Web App Builder.exe`

## Important Notes
- The `--add-data="app_icon.ico;."` flag bundles the default icon file into the exe
- The `get_bundled_icon_path()` method automatically finds the bundled icon whether running as script or exe
- Users can still choose their own custom icon, but if they don't, the bundled `app_icon.ico` is used as default

## How It Works
1. **During development**: Uses `app_icon.ico` from the script directory
2. **As exe**: PyInstaller extracts bundled files to `sys._MEIPASS` temporary folder
3. **The code**: Automatically detects if running as exe (`sys.frozen`) and adjusts the path accordingly

## Distribution
Just distribute the single `Web App Builder.exe` file - the default icon is embedded inside it!
