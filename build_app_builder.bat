@echo off
echo Building Web App Builder...
echo.

REM Check if app_icon.ico exists
if not exist "app_icon.ico" (
    echo ERROR: app_icon.ico not found!
    echo Please make sure app_icon.ico is in the current directory.
    pause
    exit /b 1
)

REM Build with PyInstaller
pyinstaller --onefile --windowed ^
    --name="Web App Builder" ^
    --icon=app_icon.ico ^
    --add-data="app_icon.ico;." ^
    --clean ^
    app_builder.py

echo.
if %ERRORLEVEL% EQU 0 (
    echo ✓ Build completed successfully!
    echo.
    echo Executable location: dist\Web App Builder.exe
    echo.
    pause
    start dist
) else (
    echo ✗ Build failed!
    pause
)
