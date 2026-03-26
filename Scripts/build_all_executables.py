#!/usr/bin/env python3
"""
Build All FluxUI Executables
Creates complete executable package for GitHub distribution
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

class FluxUIExecutableBuilder:
    def __init__(self):
        self.version = "Beta 1.0"
        self.build_dir = "dist_executables"
        self.release_dir = "FluxUI_Release"
        
    def check_pyinstaller(self):
        """Check if PyInstaller is available"""
        try:
            import PyInstaller
            return True
        except ImportError:
            print("Installing PyInstaller...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            return True
    
    def clean_build_dirs(self):
        """Clean build directories"""
        for dir_name in [self.build_dir, self.release_dir]:
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
            os.makedirs(dir_name)
    
    def build_fluxui_exe(self):
        """Build main FluxUI executable"""
        print("Building FluxUI.exe...")
        
        options = [
            "--name=FluxUI",
            "--onefile",
            "--windowed",
            "--add-data=parser.py;.",
            "--add-data=tokenizer.py;.",
            "--add-data=parser_ast.py;.",
            "--add-data=engine.py;.",
            "--add-data=ui_engine.py;.",
            "--add-data=components.py;.",
            "--add-data=renderer.py;.",
            "--add-data=flux_runner.py;.",
            "--hidden-import=tkinter",
            "--hidden-import=customtkinter",
            "--hidden-import=tkinter.ttk",
            "--hidden-import=tkinter.filedialog",
            "--hidden-import=tkinter.messagebox",
            "--distpath=fluxui_exe",
            "--workpath=build_fluxui",
            "fluxui.py"
        ]
        
        cmd = [sys.executable, "-m", "PyInstaller"] + options
        subprocess.run(cmd, check=True)
        
        # Move to build directory
        if os.path.exists("fluxui_exe/FluxUI.exe"):
            shutil.move("fluxui_exe/FluxUI.exe", f"{self.build_dir}/FluxUI.exe")
            print("✅ FluxUI.exe created")
        
        # Clean up
        if os.path.exists("fluxui_exe"):
            shutil.rmtree("fluxui_exe")
        if os.path.exists("build_fluxui"):
            shutil.rmtree("build_fluxui")
        if os.path.exists("FluxUI.spec"):
            os.remove("FluxUI.spec")
    
    def build_cli_exe(self):
        """Build FluxUI CLI executable"""
        print("Building fluxui-cli.exe...")
        
        options = [
            "--name=fluxui-cli",
            "--onefile",
            "--console",
            "--add-data=parser.py;.",
            "--add-data=tokenizer.py;.",
            "--add-data=parser_ast.py;.",
            "--add-data=engine.py;.",
            "--add-data=ui_engine.py;.",
            "--add-data=components.py;.",
            "--add-data=renderer.py;.",
            "--add-data=flux_runner.py;.",
            "--hidden-import=tkinter",
            "--hidden-import=customtkinter",
            "--distpath=cli_exe",
            "--workpath=build_cli",
            "fluxui_cli.py"
        ]
        
        cmd = [sys.executable, "-m", "PyInstaller"] + options
        subprocess.run(cmd, check=True)
        
        # Move to build directory
        if os.path.exists("cli_exe/fluxui-cli.exe"):
            shutil.move("cli_exe/fluxui-cli.exe", f"{self.build_dir}/fluxui-cli.exe")
            print("✅ fluxui-cli.exe created")
        
        # Clean up
        if os.path.exists("cli_exe"):
            shutil.rmtree("cli_exe")
        if os.path.exists("build_cli"):
            shutil.rmtree("build_cli")
        if os.path.exists("fluxui-cli.spec"):
            os.remove("fluxui-cli.spec")
        config_dir = os.path.join(os.getcwd(), 'config')
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        config = {
            "version": self.version,
            "build_dir": self.build_dir,
            "release_dir": self.release_dir
        }
        with open(os.path.join(config_dir, "config.json"), "w") as f:
            json.dump(config, f, indent=2)
    
    def build_ide_exe(self):
        """Build FluxUI IDE executable"""
        print("Building fluxui-ide.exe...")
        
        options = [
            "--name=fluxui-ide",
            "--onefile",
            "--windowed",
            "--add-data=parser.py;.",
            "--add-data=tokenizer.py;.",
            "--add-data=parser_ast.py;.",
            "--add-data=engine.py;.",
            "--add-data=ui_engine.py;.",
            "--add-data=components.py;.",
            "--add-data=renderer.py;.",
            "--add-data=flux_runner.py;.",
            "--hidden-import=tkinter",
            "--hidden-import=customtkinter",
            "--hidden-import=tkinter.ttk",
            "--hidden-import=tkinter.filedialog",
            "--hidden-import=tkinter.messagebox",
            "--distpath=ide_exe",
            "--workpath=build_ide",
            "fluxui_ide.py"
        ]
        
        cmd = [sys.executable, "-m", "PyInstaller"] + options
        subprocess.run(cmd, check=True)
        
        # Move to build directory
        if os.path.exists("ide_exe/fluxui-ide.exe"):
            shutil.move("ide_exe/fluxui-ide.exe", f"{self.build_dir}/fluxui-ide.exe")
            print("✅ fluxui-ide.exe created")
        
        # Clean up
        if os.path.exists("ide_exe"):
            shutil.rmtree("ide_exe")
        if os.path.exists("build_ide"):
            shutil.rmtree("build_ide")
        if os.path.exists("fluxui-ide.spec"):
            os.remove("fluxui-ide.spec")
    
    def build_installer_exe(self):
        """Build installer executable"""
        print("Building Installer.exe...")
        
        options = [
            "--name=FluxUI_Installer",
            "--onefile",
            "--windowed",
            "--add-data=parser.py;.",
            "--add-data=tokenizer.py;.",
            "--add-data=parser_ast.py;.",
            "--add-data=engine.py;.",
            "--add-data=ui_engine.py;.",
            "--add-data=components.py;.",
            "--add-data=renderer.py;.",
            "--add-data=flux_runner.py;.",
            "--add-data=fluxui_cli.py;.",
            "--add-data=fluxui_ide.py;.",
            "--add-data=FluxUI_Language_Reference.md;.",
            "--add-data=README.md;.",
            "--add-data=Test.flux;.",
            "--add-data=fluxui.svg;.",
            "--hidden-import=tkinter",
            "--hidden-import=customtkinter",
            "--hidden-import=tkinter.ttk",
            "--hidden-import=tkinter.filedialog",
            "--hidden-import=tkinter.messagebox",
            "--hidden-import=json",
            "--hidden-import=threading",
            "--hidden-import=winreg",
            "--distpath=installer_exe",
            "--workpath=build_installer",
            "fluxui_auto_installer.py"
        ]
        
        cmd = [sys.executable, "-m", "PyInstaller"] + options
        subprocess.run(cmd, check=True)
        
        # Move to build directory
        if os.path.exists("installer_exe/FluxUI_Installer.exe"):
            shutil.move("installer_exe/FluxUI_Installer.exe", f"{self.build_dir}/FluxUI_Installer.exe")
            print("✅ FluxUI_Installer.exe created")
        
        # Clean up
        if os.path.exists("installer_exe"):
            shutil.rmtree("installer_exe")
        if os.path.exists("build_installer"):
            shutil.rmtree("build_installer")
        if os.path.exists("FluxUI_Installer.spec"):
            os.remove("FluxUI_Installer.spec")
    
    def build_online_installer_exe(self):
        """Build online installer executable"""
        print("Building FluxUI_Online_Installer.exe...")
        
        options = [
            "--name=FluxUI_Online_Installer",
            "--onefile",
            "--windowed",
            "--hidden-import=tkinter",
            "--hidden-import=customtkinter",
            "--hidden-import=tkinter.ttk",
            "--hidden-import=tkinter.filedialog",
            "--hidden-import=tkinter.messagebox",
            "--hidden-import=json",
            "--hidden-import=threading",
            "--hidden-import=winreg",
            "--hidden-import=urllib.request",
            "--hidden-import=tempfile",
            "--distpath=online_installer_exe",
            "--workpath=build_online_installer",
            "fluxui_online_installer.py"
        ]
        
        cmd = [sys.executable, "-m", "PyInstaller"] + options
        subprocess.run(cmd, check=True)
        
        # Move to build directory
        if os.path.exists("online_installer_exe/FluxUI_Online_Installer.exe"):
            shutil.move("online_installer_exe/FluxUI_Online_Installer.exe", f"{self.build_dir}/FluxUI_Online_Installer.exe")
            print("✅ FluxUI_Online_Installer.exe created")
        
        # Clean up
        if os.path.exists("online_installer_exe"):
            shutil.rmtree("online_installer_exe")
        if os.path.exists("build_online_installer"):
            shutil.rmtree("build_online_installer")
        if os.path.exists("FluxUI_Online_Installer.spec"):
            os.remove("FluxUI_Online_Installer.spec")
    
    def build_wizard_exe(self):
        """Build interactive wizard executable"""
        print("Building FluxUI_Setup.exe...")
        
        options = [
            "--name=FluxUI_Setup",
            "--onefile",
            "--windowed",
            "--add-data=parser.py;.",
            "--add-data=tokenizer.py;.",
            "--add-data=parser_ast.py;.",
            "--add-data=engine.py;.",
            "--add-data=ui_engine.py;.",
            "--add-data=components.py;.",
            "--add-data=renderer.py;.",
            "--add-data=flux_runner.py;.",
            "--add-data=fluxui_cli.py;.",
            "--add-data=fluxui_ide.py;.",
            "--add-data=FluxUI_Language_Reference.md;.",
            "--add-data=README.md;.",
            "--add-data=Test.flux;.",
            "--add-data=fluxui.svg;.",
            "--hidden-import=tkinter",
            "--hidden-import=customtkinter",
            "--hidden-import=tkinter.ttk",
            "--hidden-import=tkinter.filedialog",
            "--hidden-import=tkinter.messagebox",
            "--hidden-import=json",
            "--hidden-import=threading",
            "--hidden-import=winreg",
            "--distpath=wizard_exe",
            "--workpath=build_wizard",
            "fluxui_wizard.py"
        ]
        
        cmd = [sys.executable, "-m", "PyInstaller"] + options
        subprocess.run(cmd, check=True)
        
        # Move to build directory
        if os.path.exists("wizard_exe/FluxUI_Setup.exe"):
            shutil.move("wizard_exe/FluxUI_Setup.exe", f"{self.build_dir}/FluxUI_Setup.exe")
            print("✅ FluxUI_Setup.exe created")
        
        # Clean up
        if os.path.exists("wizard_exe"):
            shutil.rmtree("wizard_exe")
        if os.path.exists("build_wizard"):
            shutil.rmtree("build_wizard")
        if os.path.exists("FluxUI_Setup.spec"):
            os.remove("FluxUI_Setup.spec")
    
    def create_release_package(self):
        """Create complete release package"""
        print("Creating release package...")
        
        # Create release directory structure
        release_dirs = [
            "bin",
            "docs", 
            "samples",
            "templates"
        ]
        
        for dir_name in release_dirs:
            os.makedirs(f"{self.release_dir}/{dir_name}", exist_ok=True)
        
        # Copy executables
        shutil.copy(f"{self.build_dir}/FluxUI.exe", f"{self.release_dir}/bin/")
        shutil.copy(f"{self.build_dir}/fluxui-cli.exe", f"{self.release_dir}/bin/")
        shutil.copy(f"{self.build_dir}/fluxui-ide.exe", f"{self.release_dir}/bin/")
        
        # Copy installers
        shutil.copy(f"{self.build_dir}/FluxUI_Installer.exe", self.release_dir)
        shutil.copy(f"{self.build_dir}/FluxUI_Online_Installer.exe", self.release_dir)
        shutil.copy(f"{self.build_dir}/FluxUI_Setup.exe", self.release_dir)
        
        # Copy documentation
        if os.path.exists("FluxUI_Language_Reference.md"):
            shutil.copy("FluxUI_Language_Reference.md", f"{self.release_dir}/docs/")
        if os.path.exists("README.md"):
            shutil.copy("README.md", f"{self.release_dir}/docs/")
        
        # Copy samples
        if os.path.exists("Test.flux"):
            shutil.copy("Test.flux", f"{self.release_dir}/samples/")
        if os.path.exists("test_executable.flux"):
            shutil.copy("test_executable.flux", f"{self.release_dir}/samples/")
        
        # Create basic sample
        basic_sample = '''# Basic FluxUI Application
APP "Hello World" 400 300

LABEL greeting {
    TEXT: "Hello, FluxUI!"
    FONT_SIZE: 16
    X: 20
    Y: 20
}

BUTTON btn {
    TEXT: "Click Me"
    X: 20
    Y: 60
    ONCLICK: {
        PRINT "Button clicked!"
    }
}
'''
        
        with open(f"{self.release_dir}/samples/basic.flux", "w") as f:
            f.write(basic_sample)
        
        # Create templates
        templates = {
            "basic": '''# Basic FluxUI Application
APP "{{project_name}}" 400 300

VAR message = "Hello, FluxUI!"

LABEL title {
    TEXT: message
    FONT_SIZE: 16
    X: 20
    Y: 20
}

BUTTON btn {
    TEXT: "Click Me"
    X: 20
    Y: 60
    ONCLICK: {
        PRINT "Button clicked!"
        SET message = "Button was clicked!"
        SET_TEXT title message
    }
}
''',
            "ui": '''# UI Application
APP "{{project_name}}" 800 600

VAR counter = 0

FRAME main_frame {
    WIDTH: 780
    HEIGHT: 580
    PADDING: 10
    
    LABEL title {
        TEXT: "{{project_name}}"
        FONT_SIZE: 20
        X: 10
        Y: 10
    }
    
    ROW controls {
        Y: 50
        SPACING: 10
        
        BUTTON increment_btn {
            TEXT: "Increment"
            ONCLICK: {
                SET counter += 1
                SET_TEXT counter_label "Count: " + counter
            }
        }
        
        BUTTON decrement_btn {
            TEXT: "Decrement"
            ONCLICK: {
                SET counter -= 1
                SET_TEXT counter_label "Count: " + counter
            }
        }
    }
    
    LABEL counter_label {
        TEXT: "Count: 0"
        FONT_SIZE: 14
        X: 10
        Y: 100
    }
}
'''
        }
        
        for template_name, content in templates.items():
            with open(f"{self.release_dir}/templates/{template_name}.flux", "w") as f:
                f.write(content)
        
        # Create batch files for easy access
        batch_files = {
            "run_fluxui.bat": '''@echo off
bin\\FluxUI.exe %*
''',
            "run_ide.bat": '''@echo off
bin\\fluxui-ide.exe
''',
            "run_cli.bat": '''@echo off
bin\\fluxui-cli.exe %*
'''
        }
        
        for file_name, content in batch_files.items():
            with open(f"{self.release_dir}/{file_name}", "w") as f:
                f.write(content)
        
        # Create README for release
        release_readme = f'''# FluxUI v{self.version} - Complete Executable Package

## 🚀 Quick Start

### Option 1: Online Installer (Recommended - Smallest Download)
Double-click: `FluxUI_Online_Installer.exe`
- Downloads components from GitHub during installation
- Smallest initial download size
- Always gets latest version

### Option 2: Offline Installer (Complete Package)
Double-click: `FluxUI_Installer.exe`
- Contains all components
- No internet connection required
- One-time installation

### Option 3: Interactive Setup
Double-click: `FluxUI_Setup.exe`
- Interactive wizard with options
- Choose components to install

### Option 4: Manual Usage
1. Run installer first to set up file associations
2. Use executables from `bin/` folder:
   - `FluxUI.exe` - Run .flux files
   - `fluxui-cli.exe` - Modern CLI
   - `fluxui-ide.exe` - IDE

## 📁 Package Contents

```
FluxUI_Release/
├── FluxUI_Online_Installer.exe  # ⭐ Lightweight online installer
├── FluxUI_Installer.exe         # Complete offline installer
├── FluxUI_Setup.exe             # Interactive wizard
├── bin/                         # Executables
│   ├── FluxUI.exe              # Main interpreter
│   ├── fluxui-cli.exe          # CLI tools
│   └── fluxui-ide.exe          # IDE
├── docs/                        # Documentation
├── samples/                     # Sample projects
├── templates/                   # Project templates
├── run_fluxui.bat              # Quick runner
├── run_ide.bat                 # IDE launcher
└── run_cli.bat                 # CLI launcher
```

## 🎮 Usage

### Run FluxUI Programs
```bash
# Double-click .flux files (after installer)
# Or use command line:
FluxUI.exe program.flux

# Quick batch files:
run_fluxui.bat program.flux
```

### Modern CLI
```bash
fluxui-cli.exe --help
fluxui-cli.exe new myapp
fluxui-cli.exe run program.flux
```

### IDE
```bash
# Double-click fluxui-ide.exe
# Or use batch:
run_ide.bat
```

## 📄 License

MIT License
Copyright (c) 2026 ZeroGravityGamingX211

## 🌐 Repository

https://github.com/zerogravitygamingx211-hash/FluxUI

---

FluxUI v{self.version} - Complete Programming Language Package
Author: ZeroGravityGamingX211
'''
        
        with open(f"{self.release_dir}/README.md", "w") as f:
            f.write(release_readme)
        
        print("✅ Release package created")
    
    def create_github_release(self):
        """Create GitHub-ready release files"""
        print("Creating GitHub release files...")
        
        # Create release info
        release_info = f'''# FluxUI v{self.version} Release

## 📦 Download Options

### 🎯 For Users
- **FluxUI_Online_Installer.exe** - Lightweight online installer (Recommended)
- **FluxUI_Installer.exe** - Complete offline installer
- **FluxUI_Setup.exe** - Interactive setup wizard

### 🔧 For Developers
- **FluxUI_Release.zip** - Complete package with all executables

## 🚀 What's New

### Features
- **Online Installer** - Downloads components from GitHub during installation
- Complete executable package
- Auto installer with file associations
- Modern CLI interface
- Integrated Development Environment
- Sample projects and templates
- Professional documentation

### Installation Options
1. **Online Installer** (Recommended)
   - Smallest download size
   - Downloads latest components from GitHub
   - Always up-to-date

2. **Offline Installer**
   - Complete package included
   - No internet required
   - One-time download

3. **Interactive Setup**
   - Choose installation options
   - Custom installation path

### System Requirements
- Windows 10/11
- Internet connection (for online installer)
- No additional dependencies required
- All executables are standalone

## 📁 Package Contents

### Installers
- `FluxUI_Online_Installer.exe` - Lightweight online installer
- `FluxUI_Installer.exe` - Complete offline installer
- `FluxUI_Setup.exe` - Interactive wizard

### Core Executables
- `FluxUI.exe` - Main language interpreter
- `fluxui-cli.exe` - Modern CLI interface
- `fluxui-ide.exe` - IDE with syntax highlighting

### Documentation
- Complete language reference
- Sample projects
- Project templates

## 🎮 Usage Examples

### Hello World
```flux
APP "Hello" 400 300
LABEL {{ TEXT: "Hello, FluxUI!" X: 20 Y: 20 }}
```

### Interactive UI
```flux
APP "Calculator" 300 400
VAR result = 0
BUTTON {{ TEXT: "1" ONCLICK: {{ SET result = 1 }} }}
LABEL {{ TEXT: result X: 20 Y: 100 }}
```

## 🌐 Links

- **Repository**: https://github.com/zerogravitygamingx211-hash/FluxUI
- **Documentation**: Included in package
- **Issues**: Report on GitHub

## 📄 License

MIT License - Copyright (c) 2026 ZeroGravityGamingX211

---

**Thank you for using FluxUI!** ⚡
'''
        
        with open(f"{self.release_dir}/RELEASE_NOTES.md", "w") as f:
            f.write(release_info)
        
        print("✅ GitHub release files created")
    
    def organize_github_files(self):
        """Organize files for GitHub upload"""
        print("Organizing GitHub upload files...")
        
        # Create basic structure
        github_dir = "github_upload_files"
        
        # Create directories
        dirs = [github_dir, f"{github_dir}/executables", f"{github_dir}/installers", 
                f"{github_dir}/docs", f"{github_dir}/samples", f"{github_dir}/templates"]
        
        for dir_name in dirs:
            os.makedirs(dir_name, exist_ok=True)
        
        # Copy executables
        if os.path.exists(self.build_dir):
            for file in os.listdir(self.build_dir):
                if file.endswith('.exe'):
                    shutil.copy2(f"{self.build_dir}/{file}", f"{github_dir}/executables/")
        
        # Copy documentation
        doc_files = ["FluxUI_Language_Reference.md", "README.md", "INSTALLATION_README.md"]
        for doc_file in doc_files:
            if os.path.exists(doc_file):
                shutil.copy2(doc_file, f"{github_dir}/docs/")
        
        # Copy samples
        if os.path.exists("Test.flux"):
            shutil.copy2("Test.flux", f"{github_dir}/samples/")
        
        print("✅ GitHub structure created")
    
    def build_all(self):
        """Build all executables"""
        print(f"🚀 Building FluxUI Executables v{self.version}")
        print("=" * 50)
        
        try:
            # Check dependencies
            self.check_pyinstaller()
            
            # Clean build directories
            self.clean_build_dirs()
            
            # Build all executables
            self.build_fluxui_exe()
            self.build_cli_exe()
            self.build_ide_exe()
            self.build_installer_exe()
            self.build_online_installer_exe()
            self.build_wizard_exe()
            
            # Create release package
            self.create_release_package()
            self.create_github_release()
            
            # Organize GitHub upload files
            self.organize_github_files()
            
            print("\n🎉 Build Complete!")
            print(f"📦 Executables: {self.build_dir}/")
            print(f"📁 Release Package: {self.release_dir}/")
            print("\nReady for GitHub upload!")
            
            # List created files
            print("\nCreated executables:")
            for file in os.listdir(self.build_dir):
                if file.endswith('.exe'):
                    size = os.path.getsize(f"{self.build_dir}/{file}") / (1024*1024)
                    print(f"  ✅ {file} ({size:.1f} MB)")
            
            return True
            
        except Exception as e:
            print(f"❌ Build failed: {e}")
            return False


if __name__ == "__main__":
    builder = FluxUIExecutableBuilder()
    success = builder.build_all()
    
    if success:
        print("\n🚀 Ready for GitHub release!")
        print("\nUpload these files to your GitHub repository:")
        print(f"- {builder.build_dir}/*.exe (individual executables)")
        print(f"- {builder.release_dir}/ (complete package)")
        print("- Create a new GitHub release with these files")
    else:
        sys.exit(1)
