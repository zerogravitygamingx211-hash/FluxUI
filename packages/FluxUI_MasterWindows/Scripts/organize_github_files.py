#!/usr/bin/env python3
"""
Organize GitHub Upload Files
Creates proper folder structure for GitHub repository
"""
import os
import sys
import shutil
from pathlib import Path

class GitHubFileOrganizer:
    def __init__(self):
        self.github_files_dir = "github_upload_files"
        self.executables_dir = os.path.join(self.github_files_dir, "executables")
        self.docs_dir = os.path.join(self.github_files_dir, "docs")
        self.samples_dir = os.path.join(self.github_files_dir, "samples")
        self.templates_dir = os.path.join(self.github_files_dir, "templates")
        self.installers_dir = os.path.join(self.github_files_dir, "installers")
        
    def create_structure(self):
        """Create the folder structure"""
        print("Creating GitHub upload structure...")
        
        # Create main directories
        dirs = [
            self.github_files_dir,
            self.executables_dir,
            self.docs_dir,
            self.samples_dir,
            self.templates_dir,
            self.installers_dir
        ]
        
        for dir_name in dirs:
            os.makedirs(dir_name, exist_ok=True)
            print(f"  Created: {dir_name}")
    
    def copy_executables(self):
        """Copy executable files to executables folder"""
        print("Copying executables...")
        
        # Check if dist_executables exists
        if os.path.exists("dist_executables"):
            exe_files = [f for f in os.listdir("dist_executables") if f.endswith('.exe')]
            for exe_file in exe_files:
                src = os.path.join("dist_executables", exe_file)
                dst = os.path.join(self.executables_dir, exe_file)
                if os.path.exists(src):
                    shutil.copy2(src, dst)
                    print(f"  Copied: {exe_file}")
        
        # Also copy from current directory if they exist
        local_exes = [f for f in os.listdir('.') if f.endswith('.exe') and f.startswith('FluxUI') or f.startswith('fluxui')]
        for exe_file in local_exes:
            src = exe_file
            dst = os.path.join(self.executables_dir, exe_file)
            if os.path.exists(src) and not os.path.exists(dst):
                shutil.copy2(src, dst)
                print(f"  Copied: {exe_file}")
    
    def copy_documentation(self):
        """Copy documentation files"""
        print("Copying documentation...")
        
        doc_files = [
            "FluxUI_Language_Reference.md",
            "README.md",
            "INSTALLATION_README.md",
            "SETUP_COMPLETE.md",
            "GITHUB_UPLOAD_GUIDE.md"
        ]
        
        # Check for reference.md as well
        if os.path.exists("reference.md"):
            doc_files.append("reference.md")
        elif os.path.exists("Reference.md"):
            doc_files.append("Reference.md")
        elif os.path.exists("REFERENCE.md"):
            doc_files.append("REFERENCE.md")
        
        for doc_file in doc_files:
            if os.path.exists(doc_file):
                shutil.copy2(doc_file, os.path.join(self.docs_dir, doc_file))
                print(f"  Copied: {doc_file}")
        
        # Create a prominent reference.md if it doesn't exist
        reference_path = os.path.join(self.docs_dir, "reference.md")
        if not os.path.exists(reference_path):
            self.create_comprehensive_reference(reference_path)
    
    def create_comprehensive_reference(self, reference_path):
        """Create comprehensive reference document"""
        print("  Creating comprehensive reference.md...")
        
        reference_content = '''# FluxUI Programming Language Reference

## Table of Contents

1. [Language Overview](#language-overview)
2. [Syntax Reference](#syntax-reference)
3. [Built-in Functions](#built-in-functions)
4. [UI Components](#ui-components)
5. [Event Handling](#event-handling)
6. [Data Types](#data-types)
7. [Control Flow](#control-flow)
8. [File Operations](#file-operations)
9. [Examples](#examples)

## Language Overview

FluxUI is a modern programming language designed for creating user interfaces with ease. It combines simple syntax with powerful UI capabilities.

### Key Features
- Event-driven programming
- Rich UI component library
- Modern, readable syntax
- Cross-platform support

## Syntax Reference

### Basic Structure
```flux
APP "Application Title" width height

# UI components and logic here
```

### Variable Declaration
```flux
VAR variable_name = value
LET variable_name = value
CONST variable_name = value
```

### UI Components
```flux
LABEL component_name {
    property: value
    property: value
}
```

## Built-in Functions

### System Functions
- `PRINT expression` - Output to console
- `INPUT prompt` - Get user input
- `SYS_EXEC command` - Execute system command
- `SYS_OPEN path` - Open file/application

### UI Functions
- `SHOW component` - Show UI component
- `HIDE component` - Hide UI component
- `SET_TEXT component text` - Set component text
- `GET_TEXT component` - Get component text

## UI Components

### Layout Components
- `WINDOW` - Main application window
- `FRAME` - Container for other components
- `ROW` - Horizontal layout
- `COLUMN` - Vertical layout
- `GRID` - Grid layout

### Basic Components
- `LABEL` - Text display
- `BUTTON` - Clickable button
- `INPUT` - Text input field
- `TEXTBOX` - Multi-line text input
- `SWITCH` - Toggle switch
- `SLIDER` - Numeric slider
- `PROGRESS` - Progress bar

### Advanced Components
- `DROPDOWN` - Selection dropdown
- `LISTBOX` - Item list
- `TREEVIEW` - Tree structure
- `TABLE` - Data table
- `CANVAS` - Drawing area

## Event Handling

### Event Types
```flux
BUTTON btn {
    TEXT: "Click Me"
    ONCLICK: {
        # Handle click event
        PRINT "Button clicked!"
    }
    ONCHANGE: {
        # Handle value change
    }
    ONHOVER: {
        # Handle mouse hover
    }
}
```

### Common Events
- `ONCLICK` - Click event
- `ONCHANGE` - Value change
- `ONHOVER` - Mouse hover
- `ONKEY` - Key press
- `ONFOCUS` - Focus gained
- `ONBLUR` - Focus lost

## Data Types

### Primitive Types
- `STRING` - Text values
- `NUMBER` - Numeric values
- `BOOLEAN` - True/False values
- `NULL` - Null/empty value

### Collections
- `LIST` - Ordered collection
- `DICT` - Key-value pairs

## Control Flow

### Conditional Statements
```flux
IF condition {
    # Code to execute
} ELSE {
    # Alternative code
}
```

### Loops
```flux
WHILE condition {
    # Loop code
}

FOR variable IN collection {
    # Loop code
}
```

### Functions
```flux
FUNC function_name(param1, param2) {
    # Function body
    RETURN result
}
```

## File Operations

### Reading Files
```flux
VAR content = READ_FILE "path/to/file.txt"
```

### Writing Files
```flux
WRITE_FILE "path/to/file.txt" content
```

### File System
```flux
IF FILE_EXISTS "path/to/file.txt" {
    PRINT "File exists"
}
```

## Examples

### Hello World
```flux
APP "Hello World" 400 300

LABEL greeting {
    TEXT: "Hello, FluxUI!"
    FONT_SIZE: 16
    X: 20
    Y: 20
}
```

### Interactive Counter
```flux
APP "Counter" 300 200

VAR count = 0

LABEL title {
    TEXT: "Counter Application"
    FONT_SIZE: 18
    X: 20
    Y: 20
}

LABEL count_label {
    TEXT: "Count: 0"
    FONT_SIZE: 14
    X: 20
    Y: 60
}

BUTTON increment {
    TEXT: "+"
    X: 20
    Y: 100
    ONCLICK: {
        SET count += 1
        SET_TEXT count_label "Count: " + count
    }
}
```

### Form Example
```flux
APP "User Form" 400 500

FRAME form {
    WIDTH: 380
    HEIGHT: 480
    PADDING: 10
    
    LABEL title {
        TEXT: "User Information"
        FONT_SIZE: 20
        X: 10
        Y: 10
    }
    
    LABEL name_label {
        TEXT: "Name:"
        X: 10
        Y: 50
    }
    
    INPUT name_input {
        WIDTH: 200
        X: 10
        Y: 70
    }
    
    BUTTON submit {
        TEXT: "Submit"
        X: 10
        Y: 100
        ONCLICK: {
            VAR name = GET_TEXT name_input
            PRINT "Submitted: " + name
        }
    }
}
```

## Component Properties

### Common Properties
- `TEXT` - Display text
- `WIDTH` - Component width
- `HEIGHT` - Component height
- `X` - X position
- `Y` - Y position
- `BG` - Background color
- `FG` - Foreground color
- `FONT_SIZE` - Text size
- `FONT_FAMILY` - Font family

### Layout Properties
- `PADDING` - Internal spacing
- `MARGIN` - External spacing
- `ANCHOR` - Position anchor
- `EXPAND` - Expand to fill space

## Color Values

Colors can be specified as:
- Hex: `#RRGGBB` (e.g., `#FF0000` for red)
- Names: `RED`, `BLUE`, `GREEN`, etc.
- RGB: `RGB(255, 0, 0)`

## Best Practices

1. **Use meaningful variable names**
2. **Organize UI with frames and layouts**
3. **Handle events properly**
4. **Test components individually**
5. **Use comments for complex logic**

## Error Handling

```flux
TRY {
    # Code that might fail
    VAR result = RISKY_OPERATION()
} CATCH error {
    PRINT "Error: " + error
}
```

## Advanced Topics

### Custom Components
You can create reusable UI components by defining templates and reusing them.

### Data Binding
FluxUI supports data binding between UI components and variables.

### Animations
Basic animations can be created using timers and property updates.

---

## Additional Resources

- **GitHub Repository**: https://github.com/zerogravitygamingx211-hash/FluxUI
- **Main Documentation**: FluxUI_Language_Reference.md
- **Sample Code**: samples/ directory
- **Templates**: templates/ directory

---

*FluxUI Version Beta 1.0 - Comprehensive Reference*
*Author: ZeroGravityGamingX211*
*License: MIT License*
'''
        
        with open(reference_path, "w", encoding="utf-8") as f:
            f.write(reference_content)
        print("  Created comprehensive reference.md")
    
    def copy_license(self):
        """Copy license files"""
        print("Copying license files...")
        
        # Create LICENSE file with MIT license
        license_content = """MIT License

Copyright (c) 2026 ZeroGravityGamingX211

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        
        with open(os.path.join(self.docs_dir, "LICENSE"), "w") as f:
            f.write(license_content)
        print("  Created: LICENSE")
        
        # Copy any existing license file
        if os.path.exists("LICENSE"):
            shutil.copy2("LICENSE", os.path.join(self.docs_dir, "LICENSE"))
            print("  Copied: LICENSE")
    
    def copy_samples(self):
        """Copy sample files"""
        print("Copying samples...")
        
        sample_files = [
            "Test.flux",
            "test_executable.flux"
        ]
        
        for sample_file in sample_files:
            if os.path.exists(sample_file):
                shutil.copy2(sample_file, os.path.join(self.samples_dir, sample_file))
                print(f"  Copied: {sample_file}")
        
        # Create basic sample if none exist
        if not any(os.path.exists(os.path.join(self.samples_dir, f)) for f in sample_files):
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
            
            with open(os.path.join(self.samples_dir, "basic.flux"), "w") as f:
                f.write(basic_sample)
            print("  Created: basic.flux")
    
    def copy_templates(self):
        """Copy template files"""
        print("Copying templates...")
        
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
''',
            "empty": '''# Empty FluxUI Application
APP "{{project_name}}" 400 300

# Your code here
'''
        }
        
        for template_name, content in templates.items():
            with open(os.path.join(self.templates_dir, f"{template_name}.flux"), "w") as f:
                f.write(content)
            print(f"  Created: {template_name}.flux")
    
    def copy_installers(self):
        """Copy installer files"""
        print("Copying installers...")
        
        # Copy installer executables
        installer_files = [
            "FluxUI_Installer.exe",
            "FluxUI_Online_Installer.exe", 
            "FluxUI_Setup.exe"
        ]
        
        for installer_file in installer_files:
            if os.path.exists(installer_file):
                shutil.copy2(installer_file, os.path.join(self.installers_dir, installer_file))
                print(f"  Copied: {installer_file}")
        
        # Copy installer batch files
        batch_files = [
            "Install_FluxUI.bat",
            "Install_FluxUI_Online.bat",
            "setup_fluxui.bat"
        ]
        
        for batch_file in batch_files:
            if os.path.exists(batch_file):
                shutil.copy2(batch_file, os.path.join(self.installers_dir, batch_file))
                print(f"  Copied: {batch_file}")
    
    def create_github_readme(self):
        """Create README for GitHub repository"""
        print("Creating GitHub README...")
        
        readme_content = '''# FluxUI Programming Language

![FluxUI Logo](https://raw.githubusercontent.com/zerogravitygamingx211-hash/FluxUI/main/fluxui.svg)

## Modern UI Programming Made Simple

FluxUI is a modern programming language designed for creating beautiful user interfaces with ease. With its simple syntax and powerful features, you can build desktop applications quickly and efficiently.

## Features

- Rich UI Components - Buttons, labels, frames, and more
- Event-Driven - Respond to user interactions instantly
- Simple Syntax - Easy to learn and read
- Modern IDE - Complete development environment
- Global Installation - Install system-wide
- Package Management - Ready for extensibility

## Quick Start

### Option 1: Install from GitHub (Recommended)

Download and run the online installer:
- [FluxUI_Online_Installer.exe](installers/FluxUI_Online_Installer.exe)

The installer will automatically download the latest components from this repository.

### Option 2: Download Complete Package

- [FluxUI_Installer.exe](installers/FluxUI_Installer.exe) - Complete offline installer
- [FluxUI_Setup.exe](installers/FluxUI_Setup.exe) - Interactive setup wizard

## Repository Structure

```
FluxUI/
├── executables/           # Core executables
│   ├── FluxUI.exe        # Main interpreter
│   ├── fluxui-cli.exe    # Modern CLI
│   └── fluxui-ide.exe     # IDE
├── installers/           # Installation programs
│   ├── FluxUI_Online_Installer.exe
│   ├── FluxUI_Installer.exe
│   └── FluxUI_Setup.exe
├── docs/                 # Documentation
│   ├── FluxUI_Language_Reference.md
│   ├── README.md
│   └── LICENSE
├── samples/              # Example programs
│   ├── Test.flux
│   └── basic.flux
└── templates/            # Project templates
    ├── basic.flux
    ├── ui.flux
    └── empty.flux
```

## Usage Examples

### Hello World
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

### Interactive Counter
```flux
APP "Counter" 300 200

VAR count = 0

LABEL title {
    TEXT: "Counter Application"
    FONT_SIZE: 18
    X: 20
    Y: 20
}

LABEL count_label {
    TEXT: "Count: 0"
    FONT_SIZE: 14
    X: 20
    Y: 60
}

ROW buttons {
    Y: 100
    X: 20
    SPACING: 10
    
    BUTTON increment {
        TEXT: "+"
        ONCLICK: {
            SET count += 1
            SET_TEXT count_label "Count: " + count
        }
    }
    
    BUTTON decrement {
        TEXT: "-"
        ONCLICK: {
            SET count -= 1
            SET_TEXT count_label "Count: " + count
        }
    }
}
```

## Installation

### After Installation

Once installed, you can:

1. Run .flux files - Double-click any `.flux` file to execute it
2. Use command line - `fluxui program.flux`
3. Modern CLI - `fluxui-cli new myapp`
4. Launch IDE - `fluxui-ide` or double-click desktop shortcut

### File Associations

The installer automatically associates `.flux` files with FluxUI.exe, so you can simply double-click them to run.

## Documentation

- **[Comprehensive Reference](docs/reference.md)** - Complete language reference (Very Important!)
- **[Language Reference](docs/FluxUI_Language_Reference.md)** - Detailed language documentation
- **[Installation Guide](docs/INSTALLATION_README.md)** - Detailed installation instructions
- **[Samples](samples/)** - Example programs to learn from
- **[Templates](templates/)** - Project templates to get started

### 📚 Quick Reference

For complete syntax, functions, and examples, see the **[Comprehensive Reference](docs/reference.md)** - this is the most important documentation file for FluxUI!

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](docs/LICENSE) file for details.

## Acknowledgments

- ZeroGravityGamingX211 - Creator and maintainer
- The FluxUI community for feedback and contributions

## Support

- Report Issues: GitHub Issues
- Discussions: GitHub Discussions
- Documentation: Language Reference

---

Made with love by ZeroGravityGamingX211

GitHub Repository: https://github.com/zerogravitygamingx211-hash/FluxUI
'''
        
        with open(os.path.join(self.github_files_dir, "README.md"), "w", encoding="utf-8") as f:
            f.write(readme_content)
        print("  Created: README.md")
    
    def create_upload_instructions(self):
        """Create upload instructions"""
        print("Creating upload instructions...")
        
        instructions = '''# GitHub Upload Instructions

## 📦 Files to Upload

### 🎯 Main Repository Files
Upload these to your main repository:

1. **README.md** - Main repository README
2. **LICENSE** - MIT License file
3. **fluxui.svg** - Logo/icon (if available)

### 📁 Folders to Upload
Create these folders in your repository and upload contents:

#### 📂 executables/
- FluxUI.exe - Main interpreter
- fluxui-cli.exe - Modern CLI
- fluxui-ide.exe - IDE

#### 📂 installers/
- FluxUI_Online_Installer.exe - Online installer (primary)
- FluxUI_Installer.exe - Offline installer
- FluxUI_Setup.exe - Interactive wizard
- Install_FluxUI.bat - Batch launcher
- Install_FluxUI_Online.bat - Online launcher
- setup_fluxui.bat - Setup launcher

#### 📂 docs/
- FluxUI_Language_Reference.md - Complete documentation
- README.md - Package README
- INSTALLATION_README.md - Installation guide
- SETUP_COMPLETE.md - Setup summary
- GITHUB_UPLOAD_GUIDE.md - This guide
- LICENSE - MIT License

#### 📂 samples/
- Test.flux - Comprehensive test
- test_executable.flux - Executable test
- basic.flux - Basic example

#### 📂 templates/
- basic.flux - Basic template
- ui.flux - UI template
- empty.flux - Empty template

## 🚀 GitHub Release

### Create Release
1. Go to repository → Releases → "Create a new release"
2. Tag: `v1.0.0`
3. Title: `FluxUI v1.0.0 - Complete Programming Language`
4. Description: Use the content from GITHUB_UPLOAD_GUIDE.md

### Upload Release Assets
Primary downloads:
- ✅ FluxUI_Online_Installer.exe (smallest, recommended)
- ✅ FluxUI_Installer.exe (complete offline)
- ✅ FluxUI_Setup.exe (interactive)

Additional files:
- ✅ Individual executables from executables/ folder
- ✅ Complete package as ZIP

## 📋 Upload Checklist

- [ ] Main README.md uploaded
- [ ] LICENSE uploaded
- [ ] All executables uploaded
- [ ] All installers uploaded
- [ ] Documentation uploaded
- [ ] Samples uploaded
- [ ] Templates uploaded
- [ ] GitHub release created
- [ ] Release assets uploaded
- [ ] Links tested in README

## 🎯 Result

Users will be able to:
1. Visit your GitHub repository
2. Download FluxUI_Online_Installer.exe
3. Run installer to get FluxUI
4. Start programming immediately!

Your repository will be professional and complete! 🚀
'''
        
        with open(os.path.join(self.github_files_dir, "UPLOAD_INSTRUCTIONS.md"), "w", encoding="utf-8") as f:
            f.write(instructions)
        print("  Created: UPLOAD_INSTRUCTIONS.md")
    
    def organize_all(self):
        """Organize all files"""
        print("🚀 Organizing GitHub Upload Files")
        print("=" * 40)
        
        try:
            self.create_structure()
            self.copy_executables()
            self.copy_documentation()
            self.copy_license()
            self.copy_samples()
            self.copy_templates()
            self.copy_installers()
            self.create_github_readme()
            self.create_upload_instructions()
            
            print("\n✅ Organization Complete!")
            print(f"📁 Files organized in: {self.github_files_dir}/")
            print("\n📋 Structure created:")
            
            # Show structure
            for root, dirs, files in os.walk(self.github_files_dir):
                level = root.replace(self.github_files_dir, '').count(os.sep)
                indent = ' ' * 2 * level
                print(f"{indent}{os.path.basename(root)}/")
                subindent = ' ' * 2 * (level + 1)
                for file in files:
                    print(f"{subindent}{file}")
            
            print(f"\n🚀 Ready for GitHub upload!")
            print(f"📖 See {self.github_files_dir}/UPLOAD_INSTRUCTIONS.md for details")
            
            return True
            
        except Exception as e:
            print(f"❌ Organization failed: {e}")
            return False


if __name__ == "__main__":
    organizer = GitHubFileOrganizer()
    success = organizer.organize_all()
    
    if success:
        print("\n🎉 Your FluxUI repository is now ready for GitHub!")
        print("📦 Upload the contents of 'github_upload_files/' to your repository.")
    else:
        sys.exit(1)
