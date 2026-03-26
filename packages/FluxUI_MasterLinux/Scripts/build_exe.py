#!/usr/bin/env python3
"""
Build FluxUI executable using PyInstaller
Creates a standalone fluxui.exe file
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

def build_executable():
    """Build the executable using PyInstaller"""
    
    # PyInstaller options
    options = [
        "--name=fluxui",
        "--onefile",                    # Create single executable
        "--console",                    # Console application
        "--add-data=*.flux;.",          # Include .flux files
        "--hidden-import=tkinter",       # Include tkinter
        "--hidden-import=customtkinter", # Include customtkinter
        "--distpath=dist",              # Output directory
        "--workpath=build",              # Build directory
        "--specpath=.",                 # Spec file location
        "fluxui.py"                     # Main script
    ]
    
    cmd = [sys.executable, "-m", "PyInstaller"] + options
    
    print("Building FluxUI executable...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("\nBuild successful!")
        print("Executable created: dist/fluxui.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False

def create_installer_script():
    """Create a script to copy the executable to system directory"""
    script_content = """@echo off
echo Installing FluxUI executable...

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
copy "dist\\fluxui.exe" "%DEST_DIR%\\" /Y
if %errorlevel% neq 0 (
    echo Error: Failed to copy executable
    pause
    exit /b 1
)

echo FluxUI installed successfully!
echo You can now run 'fluxui' from anywhere
echo.
pause
"""
    
    with open("install_exe.bat", "w") as f:
        f.write(script_content)
    
    print("Created install_exe.bat script")

def main():
    print("FluxUI Executable Builder")
    print("=" * 40)
    
    # Check PyInstaller
    if not check_pyinstaller():
        print("PyInstaller not found. Installing...")
        install_pyinstaller()
    
    # Build executable
    if build_executable():
        create_installer_script()
        
        print("\nNext steps:")
        print("1. Run 'install_exe.bat' as Administrator to install fluxui.exe")
        print("2. Run 'install_flux_extension.bat' to set up .flux file association")
        print("3. Test with: fluxui Test.flux")
    else:
        print("Build failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
