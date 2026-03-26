#!/usr/bin/env python3
"""
FluxUI Distribution Package Builder
Creates complete modern language distribution with installer
"""
import os
import sys
import subprocess
import shutil
import json
import zipfile
from pathlib import Path
import tempfile

class FluxUIDistributionBuilder:
    def __init__(self):
        self.version = "Beta 1.0"
        self.package_name = f"FluxUI-{self.version}"
        self.build_dir = "dist_build"
        self.package_dir = os.path.join(self.build_dir, self.package_name)
        
    def clean_build(self):
        """Clean build directory"""
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        os.makedirs(self.build_dir)
        
    def create_package_structure(self):
        """Create package directory structure"""
        print(f"Creating package structure: {self.package_dir}")
        
        # Main directories
        dirs = [
            "bin", "lib", "include", "samples", "docs", "templates", 
            "tools", "tests", "examples", "assets"
        ]
        
        for dir_name in dirs:
            os.makedirs(os.path.join(self.package_dir, dir_name), exist_ok=True)
        
        # Create subdirectories
        subdirs = {
            "lib": ["core", "ui", "parser", "runtime"],
            "samples": ["basic", "ui", "data", "games", "tools"],
            "templates": ["basic", "ui", "data", "empty"],
            "docs": ["api", "tutorials", "reference"],
            "tools": ["ide", "debugger", "profiler"],
            "assets": ["icons", "themes", "fonts"]
        }
        
        for parent, children in subdirs.items():
            for child in children:
                os.makedirs(os.path.join(self.package_dir, parent, child), exist_ok=True)
    
    def copy_core_files(self):
        """Copy core language files"""
        print("Copying core files...")
        
        # Core language files
        core_files = [
            "fluxui.py", "fluxui_cli.py", "parser.py", "tokenizer.py", 
            "parser_ast.py", "engine.py", "ui_engine.py", "components.py",
            "renderer.py", "flux_runner.py"
        ]
        
        for file in core_files:
            if os.path.exists(file):
                shutil.copy2(file, os.path.join(self.package_dir, "lib", "core"))
        
        # Copy to bin directory as executables
        shutil.copy2("fluxui.py", os.path.join(self.package_dir, "bin", "fluxui"))
        shutil.copy2("fluxui_cli.py", os.path.join(self.package_dir, "bin", "fluxui-cli"))
        
    def copy_ide_files(self):
        """Copy IDE files"""
        print("Copying IDE files...")
        
        if os.path.exists("fluxui_ide.py"):
            shutil.copy2("fluxui_ide.py", os.path.join(self.package_dir, "tools", "ide"))
            shutil.copy2("fluxui_ide.py", os.path.join(self.package_dir, "bin", "fluxui-ide"))
    
    def copy_installer(self):
        """Copy installer files"""
        print("Copying installer files...")
        
        if os.path.exists("fluxui_installer.py"):
            shutil.copy2("fluxui_installer.py", self.package_dir)
    
    def copy_documentation(self):
        """Copy documentation"""
        print("Copying documentation...")
        
        # Copy language reference
        if os.path.exists("FluxUI_Language_Reference.md"):
            shutil.copy2("FluxUI_Language_Reference.md", 
                        os.path.join(self.package_dir, "docs", "reference"))
        
        # Copy README
        if os.path.exists("README.md"):
            shutil.copy2("README.md", self.package_dir)
        
        # Create comprehensive docs
        self.create_documentation()
    
    def create_documentation(self):
        """Create documentation files"""
        
        # Getting Started Guide
        getting_started = """# FluxUI Getting Started Guide

## Welcome to FluxUI!

FluxUI is a modern programming language designed for creating beautiful user interfaces with ease.

## Installation

### Option 1: Installer (Recommended)
1. Run `fluxui_installer.py`
2. Follow the installation wizard
3. FluxUI will be installed system-wide

### Option 2: Manual Installation
1. Extract the FluxUI package
2. Add `bin` directory to your PATH
3. Run `fluxui --version` to verify installation

## Your First Program

Create a file called `hello.flux`:

```flux
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
```

Run it:
```bash
fluxui run hello.flux
```

## Creating a Project

Use the modern CLI:
```bash
fluxui new myapp
cd myapp
fluxui run main.flux
```

## IDE

Launch the FluxUI IDE:
```bash
fluxui-ide
```

## Learning Resources

- [Language Reference](reference/FluxUI_Language_Reference.md)
- [API Documentation](api/)
- [Tutorials](tutorials/)
- [Examples](../examples/)

## Community

- [FluxUI Documentation](https://fluxui-lang.org)
- [GitHub Repository](https://github.com/zerogravitygamingx211-hash/FluxUI)
- [Discord Community](https://discord.gg/fluxui)

Happy coding with FluxUI! 🚀
"""
        
        with open(os.path.join(self.package_dir, "docs", "getting-started.md"), "w") as f:
            f.write(getting_started)
        
        # API Documentation
        api_docs = """# FluxUI API Documentation

## Core API

### fluxui
Main FluxUI interpreter.

**Usage:**
```bash
fluxui <file.flux> [options]
```

**Options:**
- `--gui`: Run with GUI interface
- `--debug`: Enable debug mode
- `--version`: Show version

### fluxui-cli
Modern command-line interface.

**Commands:**
- `new <name>`: Create new project
- `run <file>`: Run program
- `build [path]`: Build executable
- `test [path]`: Run tests
- `install <pkg>`: Install packages
- `config`: Manage configuration
- `doctor`: Check system health

### fluxui-ide
Integrated Development Environment.

**Features:**
- Syntax highlighting
- Project management
- Integrated debugger
- Code completion
- Built-in terminal

## Language API

### Core Functions

#### PRINT
Output text to console.
```flux
PRINT "Hello, World!"
PRINT "Value:" variable
```

#### VAR/SET
Variable declaration and assignment.
```flux
VAR name = "FluxUI"
SET name = "Updated"
```

#### FUNC/CALL
Function definition and calling.
```flux
FUNC greet(name) {
    PRINT "Hello," name
}
CALL greet("World")
```

### UI Components

#### APP
Create application window.
```flux
APP "Title" width height
```

#### BUTTON
Create button widget.
```flux
BUTTON btn {
    TEXT: "Click Me"
    ONCLICK: { PRINT "Clicked!" }
}
```

#### LABEL
Create text label.
```flux
LABEL lbl {
    TEXT: "Hello"
    FONT_SIZE: 16
}
```

### Layout Components

#### FRAME
Container for widgets.
```flux
FRAME frame {
    WIDTH: 200
    HEIGHT: 150
    PADDING: 10
}
```

#### ROW/COLUMN
Layout containers.
```flux
ROW row {
    SPACING: 5
    # Add widgets here
}
```

### Events

#### ONCLICK
Handle click events.
```flux
ONCLICK: {
    # Event handler code
}
```

#### ONCHANGE
Handle change events.
```flux
ONCHANGE: {
    # Event handler code
}
```

## Standard Library

### Math Functions
- `ABS(x)`: Absolute value
- `SQRT(x)`: Square root
- `ROUND(x)`: Round number
- `FLOOR(x)`: Floor function
- `CEIL(x)`: Ceiling function

### String Functions
- `LEN(str)`: String length
- `UPPER(str)`: Uppercase
- `LOWER(str)`: Lowercase
- `SUBSTR(str, start, len)`: Substring

### List Functions
- `SIZE(list)`: List size
- `FIRST(list)`: First element
- `LAST(list)`: Last element
- `ADD_ITEM(list, item)`: Add item

## File I/O

### READ_FILE
Read file contents.
```flux
READ_FILE "file.txt" INTO content
```

### WRITE_FILE
Write to file.
```flux
WRITE_FILE "file.txt" "Hello, World!"
```

## System Functions

### SYS_EXEC
Execute system command.
```flux
SYS_EXEC "notepad.exe"
```

### SYS_OPEN
Open file or URL.
```flux
SYS_OPEN "https://example.com"
```

### SYS_NOTIFY
Show notification.
```flux
SYS_NOTIFY "Task completed!"
```
"""
        
        with open(os.path.join(self.package_dir, "docs", "api", "core-api.md"), "w") as f:
            f.write(api_docs)
    
    def create_samples(self):
        """Create sample projects"""
        print("Creating sample projects...")
        
        samples = {
            "basic": {
                "main.flux": '''# Basic FluxUI Application
APP "Basic App" 400 300

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
                "README.md": """# Basic Application

A simple FluxUI application demonstrating basic UI components.

## Features
- Text label
- Interactive button
- Variable updates

## Running
```bash
fluxui run main.flux
```
"""
            },
            "calculator": {
                "main.flux": '''# Calculator Application
APP "Calculator" 300 400

VAR display = "0"
VAR first_num = 0
VAR operation = ""
VAR new_input = TRUE

FRAME main_frame {
    WIDTH: 280
    HEIGHT: 380
    PADDING: 10
    
    TEXTBOX display_box {
        TEXT: display
        WIDTH: 260
        HEIGHT: 40
        FONT_SIZE: 18
        READONLY: TRUE
        X: 10
        Y: 10
    }
    
    ROW button_row1 {
        Y: 60
        SPACING: 5
        
        BUTTON btn7 { TEXT: "7" WIDTH: 60 HEIGHT: 50 ONCLICK: { append_digit("7") } }
        BUTTON btn8 { TEXT: "8" WIDTH: 60 HEIGHT: 50 ONCLICK: { append_digit("8") } }
        BUTTON btn9 { TEXT: "9" WIDTH: 60 HEIGHT: 50 ONCLICK: { append_digit("9") } }
        BUTTON btn_div { TEXT: "/" WIDTH: 60 HEIGHT: 50 ONCLICK: { set_op("/") } }
    }
    
    ROW button_row2 {
        Y: 120
        SPACING: 5
        
        BUTTON btn4 { TEXT: "4" WIDTH: 60 HEIGHT: 50 ONCLICK: { append_digit("4") } }
        BUTTON btn5 { TEXT: "5" WIDTH: 60 HEIGHT: 50 ONCLICK: { append_digit("5") } }
        BUTTON btn6 { TEXT: "6" WIDTH: 60 HEIGHT: 50 ONCLICK: { append_digit("6") } }
        BUTTON btn_mul { TEXT: "*" WIDTH: 60 HEIGHT: 50 ONCLICK: { set_op("*") } }
    }
    
    ROW button_row3 {
        Y: 180
        SPACING: 5
        
        BUTTON btn1 { TEXT: "1" WIDTH: 60 HEIGHT: 50 ONCLICK: { append_digit("1") } }
        BUTTON btn2 { TEXT: "2" WIDTH: 60 HEIGHT: 50 ONCLICK: { append_digit("2") } }
        BUTTON btn3 { TEXT: "3" WIDTH: 60 HEIGHT: 50 ONCLICK: { append_digit("3") } }
        BUTTON btn_sub { TEXT: "-" WIDTH: 60 HEIGHT: 50 ONCLICK: { set_op("-") } }
    }
    
    ROW button_row4 {
        Y: 240
        SPACING: 5
        
        BUTTON btn0 { TEXT: "0" WIDTH: 60 HEIGHT: 50 ONCLICK: { append_digit("0") } }
        BUTTON btn_dot { TEXT: "." WIDTH: 60 HEIGHT: 50 ONCLICK: { append_digit(".") } }
        BUTTON btn_eq { TEXT: "=" WIDTH: 60 HEIGHT: 50 ONCLICK: { calculate() } }
        BUTTON btn_add { TEXT: "+" WIDTH: 60 HEIGHT: 50 ONCLICK: { set_op("+") } }
    }
    
    BUTTON btn_clear {
        TEXT: "C"
        WIDTH: 260
        HEIGHT: 40
        Y: 300
        ONCLICK: { clear_display() }
    }
}

FUNC append_digit(digit) {
    IF new_input {
        SET display = digit
        SET new_input = FALSE
    } ELSE {
        SET display = display + digit
    }
    SET_TEXT display_box display
}

FUNC set_op(op) {
    SET first_num = TO_NUMBER(display)
    SET operation = op
    SET new_input = TRUE
}

FUNC calculate() {
    VAR second_num = TO_NUMBER(display)
    VAR result = 0
    
    IF operation == "+" {
        SET result = first_num + second_num
    } ELIF operation == "-" {
        SET result = first_num - second_num
    } ELIF operation == "*" {
        SET result = first_num * second_num
    } ELIF operation == "/" {
        SET result = first_num / second_num
    }
    
    SET display = TO_STRING(result)
    SET_TEXT display_box display
    SET new_input = TRUE
}

FUNC clear_display() {
    SET display = "0"
    SET first_num = 0
    SET operation = ""
    SET new_input = TRUE
    SET_TEXT display_box display
}
''',
                "README.md": """# Calculator

A fully functional calculator built with FluxUI.

## Features
- Basic arithmetic operations
- Clear function
- Interactive buttons
- Real-time display updates

## Running
```bash
fluxui run main.flux
```
"""
            },
            "data_viz": {
                "main.flux": '''# Data Visualization Application
APP "Data Visualization" 1000 700

VAR sales_data = [
    ["Jan", 100], ["Feb", 150], ["Mar", 120],
    ["Apr", 200], ["May", 180], ["Jun", 250]
]

FRAME main_frame {
    WIDTH: 980
    HEIGHT: 680
    PADDING: 10
    
    LABEL title {
        TEXT: "Sales Data Visualization"
        FONT_SIZE: 20
        X: 10
        Y: 10
    }
    
    LINE_PLOT sales_chart {
        WIDTH: 450
        HEIGHT: 300
        TITLE: "Monthly Sales Trend"
        X_LABEL: "Month"
        Y_LABEL: "Sales ($)"
        X: 10
        Y: 50
        DATA: sales_data
    }
    
    BAR_CHART sales_bar {
        WIDTH: 450
        HEIGHT: 300
        TITLE: "Sales by Month"
        X: 500
        Y: 50
        CATEGORIES: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        VALUES: [100, 150, 120, 200, 180, 250]
    }
    
    BUTTON refresh_btn {
        TEXT: "Refresh Data"
        X: 10
        Y: 370
        ONCLICK: {
            PRINT "Data refreshed!"
        }
    }
}
''',
                "README.md": """# Data Visualization

Demonstrates FluxUI's charting capabilities.

## Features
- Line plots
- Bar charts
- Interactive data visualization
- Professional layout

## Running
```bash
fluxui run main.flux
```
"""
            }
        }
        
        for sample_name, files in samples.items():
            sample_dir = os.path.join(self.package_dir, "samples", sample_name)
            os.makedirs(sample_dir, exist_ok=True)
            
            for file_name, content in files.items():
                with open(os.path.join(sample_dir, file_name), "w") as f:
                    f.write(content)
    
    def create_templates(self):
        """Create project templates"""
        print("Creating project templates...")
        
        templates = {
            "basic": {
                "template.json": {
                    "name": "Basic Application",
                    "description": "Simple FluxUI application with basic UI",
                    "files": ["main.flux", "README.md"]
                },
                "main.flux": '''# Basic FluxUI Application
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
                "README.md": """# {{project_name}}

A basic FluxUI application.

## Getting Started
```bash
fluxui run main.flux
```
"""
            },
            "ui": {
                "template.json": {
                    "name": "UI Application",
                    "description": "Full-featured UI application with multiple components",
                    "files": ["main.flux", "README.md"]
                },
                "main.flux": '''# UI Application
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
        
        BUTTON reset_btn {
            TEXT: "Reset"
            ONCLICK: {
                SET counter = 0
                SET_TEXT counter_label "Count: 0"
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
''',
                "README.md": """# {{project_name}}

A full-featured UI application.

## Features
- Interactive controls
- State management
- Professional layout

## Getting Started
```bash
fluxui run main.flux
```
"""
            }
        }
        
        for template_name, files in templates.items():
            template_dir = os.path.join(self.package_dir, "templates", template_name)
            os.makedirs(template_dir, exist_ok=True)
            
            for file_name, content in files.items():
                file_path = os.path.join(template_dir, file_name)
                if file_name.endswith(".json"):
                    with open(file_path, "w") as f:
                        json.dump(content, f, indent=2)
                else:
                    with open(file_path, "w") as f:
                        f.write(content)
    
    def create_build_scripts(self):
        """Create build and installation scripts"""
        print("Creating build scripts...")
        
        # Windows installer script
        install_bat = '''@echo off
echo Installing FluxUI Programming Language...

REM Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Please run this script as Administrator
    pause
    exit /b 1
)

REM Set installation directory
set "INSTALL_DIR=%ProgramFiles%\\FluxUI"

REM Create installation directory
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
)

REM Copy files
echo Copying files...
xcopy /E /I /Y "*" "%INSTALL_DIR%"

REM Add to PATH
echo Adding to PATH...
setx PATH "%PATH%;%INSTALL_DIR%\\bin" /M

REM Create file association
echo Setting up file association...
assoc .flux=FluxUIFile
ftype FluxUIFile="%INSTALL_DIR%\\bin\\fluxui.exe" "%%1"

REM Create desktop shortcut
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%Public%\\Desktop\\FluxUI IDE.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\bin\\fluxui-ide.exe'; $Shortcut.Save()"

REM Create Start Menu shortcut
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%ProgramData%\\Microsoft\\Windows\\Start Menu\\Programs\\FluxUI IDE.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\bin\\fluxui-ide.exe'; $Shortcut.Save()"

echo.
echo Installation complete!
echo.
echo FluxUI has been installed to: %INSTALL_DIR%
echo.
echo You can now:
echo - Run "fluxui --version" from command line
echo - Double-click .flux files to open them
echo - Launch FluxUI IDE from desktop or Start Menu
echo.
pause
'''
        
        with open(os.path.join(self.package_dir, "install.bat"), "w") as f:
            f.write(install_bat)
        
        # Unix/Linux install script
        install_sh = '''#!/bin/bash
echo "Installing FluxUI Programming Language..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root (use sudo)"
    exit 1
fi

# Set installation directory
INSTALL_DIR="/opt/fluxui"

# Create installation directory
mkdir -p "$INSTALL_DIR"

# Copy files
echo "Copying files..."
cp -r . "$INSTALL_DIR/"

# Make executables executable
chmod +x "$INSTALL_DIR/bin/fluxui"
chmod +x "$INSTALL_DIR/bin/fluxui-cli"
chmod +x "$INSTALL_DIR/bin/fluxui-ide"

# Create symlinks
echo "Creating symlinks..."
ln -sf "$INSTALL_DIR/bin/fluxui" "/usr/local/bin/fluxui"
ln -sf "$INSTALL_DIR/bin/fluxui-cli" "/usr/local/bin/fluxui-cli"
ln -sf "$INSTALL_DIR/bin/fluxui-ide" "/usr/local/bin/fluxui-ide"

# Create desktop entry
echo "Creating desktop entry..."
cat > /usr/share/applications/fluxui-ide.desktop << EOF
[Desktop Entry]
Name=FluxUI IDE
Comment=FluxUI Integrated Development Environment
Exec=/usr/local/bin/fluxui-ide
Icon=/opt/fluxui/assets/icons/fluxui-icon.png
Terminal=false
Type=Application
Categories=Development;IDE;
EOF

# Set up file association
echo "Setting up file association..."
echo "application/x-fluxui=fluxui-ide.desktop" >> /etc/mime.types
update-mime-database /usr/share/mime

echo ""
echo "Installation complete!"
echo ""
echo "FluxUI has been installed to: $INSTALL_DIR"
echo ""
echo "You can now:"
echo "- Run 'fluxui --version' from command line"
echo "- Launch FluxUI IDE from applications menu"
echo "- Double-click .flux files to open them"
echo ""
'''
        
        with open(os.path.join(self.package_dir, "install.sh"), "w") as f:
            f.write(install_sh)
    
    def create_package_info(self):
        """Create package information files"""
        print("Creating package information...")
        
        # Package manifest
        manifest = {
            "name": "FluxUI",
            "version": self.version,
            "description": "Modern UI Programming Language",
            "author": "FluxUI Team",
            "license": "MIT",
            "homepage": "https://fluxui-lang.org",
            "repository": "https://github.com/zerogravitygamingx211-hash/FluxUI",
            "components": {
                "core": {
                    "description": "FluxUI language interpreter",
                    "files": ["fluxui", "parser.py", "tokenizer.py", "engine.py"]
                },
                "cli": {
                    "description": "Modern command-line interface",
                    "files": ["fluxui-cli"]
                },
                "ide": {
                    "description": "Integrated Development Environment",
                    "files": ["fluxui-ide"]
                },
                "samples": {
                    "description": "Sample projects and examples",
                    "files": ["samples/"]
                },
                "docs": {
                    "description": "Documentation and guides",
                    "files": ["docs/"]
                }
            },
            "requirements": {
                "python": ">=3.7",
                "dependencies": ["customtkinter", "pyinstaller"]
            },
            "platforms": ["Windows", "Linux", "macOS"]
        }
        
        with open(os.path.join(self.package_dir, "package.json"), "w") as f:
            json.dump(manifest, f, indent=2)
        
        # Version info
        version_info = f"""FluxUI Programming Language
Version: {self.version}
Build Date: {subprocess.check_output(['date'], text=True).strip()}
Platform: {sys.platform}
Python: {sys.version}

© 2024 FluxUI Project. All rights reserved.
"""
        
        with open(os.path.join(self.package_dir, "VERSION"), "w") as f:
            f.write(version_info)
    
    def create_executables(self):
        """Create executable files"""
        print("Creating executables...")
        
        # Create executable wrappers
        executables = {
            "fluxui": "#!/usr/bin/env python3\nimport sys\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../lib/core')\nfrom fluxui import main\nif __name__ == '__main__': main()",
            "fluxui-cli": "#!/usr/bin/env python3\nimport sys\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../lib/core')\nfrom fluxui_cli import FluxUICLI\nif __name__ == '__main__': FluxUICLI().run()",
            "fluxui-ide": "#!/usr/bin/env python3\nimport sys\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../tools/ide')\nfrom fluxui_ide import FluxUIIDE\nif __name__ == '__main__': FluxUIIDE().run()"
        }
        
        for exe_name, content in executables.items():
            exe_path = os.path.join(self.package_dir, "bin", exe_name)
            with open(exe_path, "w") as f:
                f.write(content.replace("os.path.dirname(os.path.abspath(__file__))", f"'{os.path.join(self.package_dir)}'"))
            os.chmod(exe_path, 0o755)
    
    def create_zip_package(self):
        """Create ZIP package"""
        print("Creating ZIP package...")
        
        zip_path = f"{self.package_name}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.package_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_path = os.path.relpath(file_path, self.build_dir)
                    zipf.write(file_path, arc_path)
        
        print(f"ZIP package created: {zip_path}")
        return zip_path
    
    def build_installer(self):
        """Build installer executable"""
        print("Building installer...")
        
        # Copy installer to build directory
        if os.path.exists("fluxui_installer.py"):
            shutil.copy2("fluxui_installer.py", self.build_dir)
        
        print("Installer ready: fluxui_installer.py")
    
    def build_all(self):
        """Build complete distribution"""
        print(f"Building FluxUI Distribution v{self.version}")
        print("=" * 50)
        
        try:
            self.clean_build()
            self.create_package_structure()
            self.copy_core_files()
            self.copy_ide_files()
            self.copy_installer()
            self.copy_documentation()
            self.create_samples()
            self.create_templates()
            self.create_build_scripts()
            self.create_package_info()
            self.create_executables()
            
            zip_package = self.create_zip_package()
            self.build_installer()
            
            print("\nDistribution build complete!")
            print(f"Package: {zip_package}")
            print(f"Installer: {self.build_dir}/fluxui_installer.py")
            print(f"Build directory: {self.build_dir}")
            
            return True
            
        except Exception as e:
            print(f"Build failed: {e}")
            return False


if __name__ == "__main__":
    builder = FluxUIDistributionBuilder()
    success = builder.build_all()
    
    if success:
        print("\nReady to distribute FluxUI!")
        print("\nNext steps:")
        print("1. Test the installer: python dist_build/fluxui_installer.py")
        print("2. Build executables: python build_exe.py && python build_ide.py")
        print("3. Distribute the ZIP package and installer")
    else:
        sys.exit(1)
