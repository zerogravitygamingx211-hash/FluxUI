#!/usr/bin/env python3
"""
Build FluxUI IDE executable using PyInstaller
Creates a standalone fluxui_ide.exe file
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

def build_ide_executable():
    """Build the IDE executable using PyInstaller"""
    
    # PyInstaller options
    options = [
        "--name=FluxUI_IDE",
        "--onefile",                    # Create single executable
        "--windowed",                   # Windowed application (no console)
        "--add-data=*.flux;.",          # Include .flux files
        "--add-data=FluxUI_Language_Reference.md;.",  # Include documentation
        "--hidden-import=tkinter",       # Include tkinter
        "--hidden-import=customtkinter", # Include customtkinter
        "--hidden-import=tkinter.ttk",  # Include ttk
        "--hidden-import=tkinter.filedialog",  # Include filedialog
        "--hidden-import=tkinter.messagebox",  # Include messagebox
        "--distpath=dist",              # Output directory
        "--workpath=build_ide",         # Build directory
        "--specpath=.",                 # Spec file location
        "fluxui_ide.py"                 # Main script
    ]
    
    cmd = [sys.executable, "-m", "PyInstaller"] + options
    
    print("Building FluxUI IDE executable...")
    print(f"Command: {' '.join(cmd)}")
    
    try:
        subprocess.check_call(cmd)
        print("\nBuild successful!")
        print("IDE executable created: dist/FluxUI_IDE.exe")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False

def create_ide_installer_script():
    """Create a script to install the IDE"""
    script_content = """@echo off
echo Installing FluxUI IDE...

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
copy "dist\\FluxUI_IDE.exe" "%DEST_DIR%\\" /Y
if %errorlevel% neq 0 (
    echo Error: Failed to copy IDE executable
    pause
    exit /b 1
)

REM Create desktop shortcut
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\FluxUI IDE.lnk'); $Shortcut.TargetPath = '%DEST_DIR%\\FluxUI_IDE.exe'; $Shortcut.Save()"

REM Set up file association
assoc .flux=FluxUIFile
ftype FluxUIFile="FluxUI_IDE.exe" "%%1"

echo FluxUI IDE installed successfully!
echo - IDE executable: %DEST_DIR%\\FluxUI_IDE.exe
echo - Desktop shortcut created
echo - .flux file association set
echo.
echo You can now:
echo - Double-click .flux files to open in IDE
echo - Run "FluxUI_IDE" from command line
echo.
pause
"""
    
    with open("install_ide.bat", "w") as f:
        f.write(script_content)
    
    print("Created install_ide.bat script")

def create_developer_package():
    """Create a complete developer package"""
    print("Creating FluxUI Developer Package...")
    
    # Create package directory
    package_dir = "FluxUI_Developer_Package"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    os.makedirs(package_dir)
    
    # Copy essential files
    files_to_copy = [
        "fluxui.py",
        "fluxui_ide.py", 
        "flux_runner.py",
        "parser.py",
        "tokenizer.py",
        "parser_ast.py",
        "engine.py",
        "ui_engine.py",
        "components.py",
        "renderer.py",
        "build_exe.py",
        "build_ide.py",
        "install_flux_extension.bat",
        "install_exe.bat",
        "install_ide.bat",
        "generate_pdf.py",
        "FluxUI_Language_Reference.md",
        "README.md",
        "Test.flux"
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(package_dir, file))
    
    # Create package README
    package_readme = """# FluxUI Developer Package

## Complete FluxUI Development Environment

This package contains everything you need to develop FluxUI applications.

## Installation

1. **Install Dependencies**
   ```bash
   pip install customtkinter pyinstaller markdown weasyprint
   ```

2. **Build Executables**
   ```bash
   python build_exe.py    # Build fluxui.exe
   python build_ide.py    # Build FluxUI_IDE.exe
   ```

3. **Install System-wide**
   ```bash
   # Run as Administrator
   install_exe.bat       # Install fluxui.exe
   install_ide.bat        # Install FluxUI_IDE.exe
   install_flux_extension.bat  # Set .flux association
   ```

## Files Included

- **fluxui.py** - Main language executable
- **fluxui_ide.py** - Integrated Development Environment
- **parser.py, tokenizer.py, etc.** - Language core files
- **Test.flux** - Example and test file
- **FluxUI_Language_Reference.md** - Complete documentation
- **build_*.py** - Build scripts
- **install_*.bat** - Installation scripts

## Usage

### Command Line
```bash
fluxui program.flux          # Run program
fluxui --version              # Show version
```

### IDE
```bash
FluxUI_IDE                    # Launch IDE
# Or double-click desktop shortcut
```

### File Association
- Double-click `.flux` files to open in IDE
- Right-click .flux files for more options

## Development

1. Open FluxUI_IDE
2. Create new project with Project Wizard
3. Write your FluxUI code
4. Run directly from IDE
5. Build executable when ready

## Documentation

- See `FluxUI_Language_Reference.md` for complete language reference
- Use the IDE's Language Reference menu item

## Support

Check the documentation and test files for examples and guidance.

---

**FluxUI Version Beta 1.0** - Complete Development Package
"""
    
    with open(os.path.join(package_dir, "README.md"), "w") as f:
        f.write(package_readme)
    
    print(f"Developer package created: {package_dir}")

def main():
    print("FluxUI IDE Builder")
    print("=" * 40)
    
    # Check PyInstaller
    if not check_pyinstaller():
        print("PyInstaller not found. Installing...")
        install_pyinstaller()
    
    # Build IDE executable
    if build_ide_executable():
        create_ide_installer_script()
        create_developer_package()
        
        print("\nIDE Build Complete!")
        print("\nNext steps:")
        print("1. Run 'install_ide.bat' as Administrator to install IDE")
        print("2. The IDE will be available as 'FluxUI_IDE.exe'")
        print("3. Desktop shortcut will be created")
        print("4. .flux files will open in the IDE")
        print("\nDeveloper package created in 'FluxUI_Developer_Package' folder")
    else:
        print("Build failed. Check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
