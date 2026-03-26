#!/usr/bin/env python3
"""
Build FluxIDE executable using PyInstaller
Creates a standalone FluxIDE.exe file from fluxui_ide.py
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Install PyInstaller"""
    print("Installing PyInstaller...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_fluxide_executable():
    """Build the FluxIDE executable using PyInstaller"""
    
    # PyInstaller options for FluxIDE
    options = [
        "--name=FluxIDE",                 # Name the executable FluxIDE.exe
        "--onefile",                      # Create single executable
        "--windowed",                     # Windowed application (no console)
        "--add-data=*.flux;.",            # Include .flux files
        "--add-data=FluxUI_Language_Reference.md;.",  # Include language reference
        "--add-data=fluxui_icons.json;.", # Include icons config
        "--hidden-import=tkinter",         # Include tkinter
        "--hidden-import=customtkinter",  # Include customtkinter
        "--hidden-import=tkinter.ttk",     # Include ttk
        "--hidden-import=tkinter.filedialog",  # Include filedialog
        "--hidden-import=tkinter.messagebox",   # Include messagebox
        "--hidden-import=tkinter.scrolledtext", # Include scrolledtext if needed
        # "--icon=fluxui.ico",              # Use icon if available (commented out - doesn't exist)
        "--distpath=dist_executables",    # Output directory
        "--workpath=build_ide",           # Build directory
        "--specpath=.",                   # Spec file location
        "fluxui_ide.py"                   # Main script
    ]
    
    cmd = [sys.executable, "-m", "PyInstaller"] + options
    
    print("Building FluxIDE executable...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("\nBuild successful!")
        print("Executable created: dist_executables/FluxIDE.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False

def create_fluxide_installer_script():
    """Create a script to copy the FluxIDE executable"""
    script_content = """@echo off
echo Installing FluxIDE executable...

REM Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Please run this script as Administrator to install to system directory
    echo Installing to user directory instead...
    set "DEST_DIR=%USERPROFILE%\\bin"
) else (
    set "DEST_DIR=C:\\Windows\\System32"
)

REM Create destination directory if it doesn't exist
if not exist "%DEST_DIR%" (
    mkdir "%DEST_DIR%"
)

REM Copy executable
copy "dist_executables\\FluxIDE.exe" "%DEST_DIR%\\" /Y
if %errorlevel% neq 0 (
    echo Error: Failed to copy executable
    pause
    exit /b 1
)

echo FluxIDE installed successfully!
echo You can now run 'FluxIDE' from anywhere
echo.
pause
"""
    
    with open("install_FluxIDE.bat", "w") as f:
        f.write(script_content)
    
    print("Created install_FluxIDE.bat script")

def create_desktop_shortcut():
    """Create a script to add desktop shortcut"""
    script_content = """@echo off
echo Creating FluxIDE desktop shortcut...

set "SHORTCUT=%USERPROFILE%\\Desktop\\FluxIDE.lnk"
set "TARGET=%CD%\\dist_executables\\FluxIDE.exe"

powershell -command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT%'); $s.TargetPath = '%TARGET%'; $s.Save()"

echo Desktop shortcut created: %SHORTCUT%
pause
"""
    
    with open("add_FluxIDE_shortcut.bat", "w") as f:
        f.write(script_content)
    
    print("Created add_FluxIDE_shortcut.bat script")

def main():
    print("FluxIDE Executable Builder")
    print("=" * 40)
    
    # Check if fluxui_ide.py exists
    if not os.path.exists("fluxui_ide.py"):
        print("Error: fluxui_ide.py not found in current directory")
        sys.exit(1)
    
    # Check PyInstaller
    if not check_pyinstaller():
        print("PyInstaller not found. Installing...")
        install_pyinstaller()
    
    # Build executable
    if build_fluxide_executable():
        create_fluxide_installer_script()
        create_desktop_shortcut()
        
        print("\nBuild completed successfully!")
        print("\nNext steps:")
        print("1. Run 'install_FluxIDE.bat' as Administrator to install FluxIDE.exe to system path")
        print("2. Run 'add_FluxIDE_shortcut.bat' to create a desktop shortcut")
        print("3. Or directly run: dist_executables\\FluxIDE.exe")
        print("\nFluxIDE can also be started from the command line with: FluxIDE")
    else:
        print("Build failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
