# FluxUI - Modern UI Programming Language

FluxUI is a high-level programming language designed for creating user interfaces with ease. It combines traditional programming constructs with a rich set of UI widgets and event handling capabilities.

## � Repository Structure

```
FluxUI/
├── Scripts/                 # All Python source files
│   ├── fluxui.py           # Main FluxUI interpreter
│   ├── fluxui_ide.py       # FluxIDE IDE application
│   ├── build_*.py          # Build and packaging scripts
│   └── *.py                # Other Python modules
├── Sh/                     # Batch and shell scripts
│   ├── *.bat               # Windows batch files
│   ├── *.sh                # Linux shell scripts
│   └── README.md           # Scripts documentation
├── FluxIDE_Release/        # FluxIDE standalone executable
│   ├── FluxIDE.zip         # Compressed IDE (29MB)
│   └── README.md           # IDE installation guide
├── packages/               # Platform-specific packages
│   ├── FluxUI_MasterWindows.zip
│   └── FluxUI_MasterLinux.zip
└── *.md                    # Documentation files
```

## 🚀 Quick Downloads

### **🖥️ Download Windows**
[![Download Windows](https://img.shields.io/badge/Download-Windows-blue?style=for-the-badge&logo=windows)](https://github.com/zerogravitygamingx211-hash/FluxUI/archive/refs/heads/master.zip)
*Complete FluxUI source package for Windows*

**Windows Package Contents:**
- [FluxIDE.exe](https://raw.githubusercontent.com/zerogravitygamingx211-hash/FluxUI/master/packages/FluxUI_MasterWindows/FluxIDE.exe) - Standalone IDE
- [FluxIDE.zip](https://raw.githubusercontent.com/zerogravitygamingx211-hash/FluxUI/master/packages/FluxUI_MasterWindows/FluxIDE.zip) - Compressed IDE
- [Installation Guide](https://raw.githubusercontent.com/zerogravitygamingx211-hash/FluxUI/master/packages/FluxUI_MasterWindows/README_Windows.md)

### **🐧 Download Linux** 
[![Download Linux](https://img.shields.io/badge/Download-Linux-orange?style=for-the-badge&logo=linux)](https://github.com/zerogravitygamingx211-hash/FluxUI/archive/refs/heads/master.zip)
*Complete FluxUI source package for Linux*

**Linux Package Contents:**
- [FluxIDE.exe](https://raw.githubusercontent.com/zerogravitygamingx211-hash/FluxUI/master/packages/FluxUI_MasterLinux/FluxIDE.exe) - Standalone IDE
- [FluxIDE.zip](https://raw.githubusercontent.com/zerogravitygamingx211-hash/FluxUI/master/packages/FluxUI_MasterLinux/FluxIDE.zip) - Compressed IDE
- [Installation Guide](https://raw.githubusercontent.com/zerogravitygamingx211-hash/FluxUI/master/packages/FluxUI_MasterLinux/README_Linux.md)

### **💻 Download FluxIDE**
[![Download FluxIDE](https://img.shields.io/badge/Download-FluxIDE-green?style=for-the-badge&logo=visual-studio-code)](https://raw.githubusercontent.com/zerogravitygamingx211-hash/FluxUI/master/FluxIDE_Release/FluxIDE.zip)
*Standalone IDE for FluxUI development (29MB)*

### **📦 Download Complete Package**
[![Download Complete](https://img.shields.io/badge/Download-Complete_Package-purple?style=for-the-badge&logo=github)](https://github.com/zerogravitygamingx211-hash/FluxUI/archive/refs/heads/master.zip)
*Entire repository with all packages and tools*

---

## Package Details

## Quick Start

### Installation

#### **Method 1: Package Installation (Recommended)**

**Windows:**
1. Download `FluxUI_MasterWindows.zip`
2. Extract and run `FluxUI_Installer.exe` as administrator
3. Follow installation steps

**Linux:**
1. Download `FluxUI_MasterLinux.zip`
2. Extract: `tar -xzf FluxUI_MasterLinux.zip`
3. Run: `sudo ./install_global.sh`

#### **Method 2: Manual Installation**

1. **Install Dependencies**
   ```bash
   pip install customtkinter pyinstaller markdown weasyprint
   ```

2. **Build Executable**
   ```bash
   python build_exe.py
   ```

3. **Install System-wide**
   ```bash
   # Run as Administrator
   install_exe.bat
   ```

4. **Set Up File Association**
   ```bash
   # Run as Administrator
   install_flux_extension.bat
   ```

### Usage

```bash
# Execute a FluxUI file
fluxui program.flux

# Execute with GUI interface
fluxui program.flux --gui

# Show version
fluxui --version
```

## Features

- **Simple Syntax**: Clean, readable syntax inspired by modern languages
- **Rich UI Components**: Extensive widget library for modern interfaces
- **Event-Driven**: Comprehensive event handling system
- **Cross-Platform**: Built on Python with CustomTkinter
- **Graphics Support**: Built-in charting and visualization capabilities
- **File Operations**: Native file I/O support
- **Error Handling**: Robust try/catch exception handling

## Language Overview

### Basic Syntax
```flux
# Variables
VAR name = "FluxUI"
VAR version = 1.0
VAR active = TRUE

# Control Flow
IF version >= 1.0 {
    PRINT "Modern version"
}

# Loops
FOR i FROM 1 TO 5 {
    PRINT i
}

# Functions
FUNC greet(name) {
    PRINT "Hello," name
}
```

### UI Components
```flux
APP "My App" 400 300

BUTTON btn1 {
    TEXT: "Click Me"
    ONCLICK: {
        PRINT "Button clicked!"
    }
}
```

## Documentation

- **Language Reference**: `FluxUI_Language_Reference.md`
- [FluxUI Documentation](https://fluxui-lang.org)
- [GitHub Repository](https://github.com/zerogravitygamingx211-hash/FluxUI) 
- **PDF Documentation**: Run `python generate_pdf.py` to create PDF

## File Structure

```
FluxUI/
├── fluxui.py                 # Main executable entry point
├── flux_runner.py            # Headless execution engine
├── ui_engine.py              # GUI execution engine
├── parser.py                 # Language parser
├── tokenizer.py              # Lexical analyzer
├── parser_ast.py             # Abstract syntax tree
├── engine.py                 # Runtime engine
├── components.py             # UI components
├── renderer.py               # UI renderer
├── Test.flux                 # Test file with examples
├── build_exe.py              # Build script for executable
├── install_flux_extension.bat # File association setup
├── install_exe.bat          # System installation script
├── generate_pdf.py          # PDF documentation generator
├── FluxUI_Language_Reference.md # Complete language reference
└── README.md                # This file
```

## Building from Source

1. **Clone/Download** the FluxUI project
2. **Install dependencies**: `pip install customtkinter pyinstaller`
3. **Build executable**: `python build_exe.py`
4. **Install system-wide**: `install_exe.bat` (as Administrator)
5. **Set up file association**: `install_flux_extension.bat` (as Administrator)

## Testing

Run the test file to verify installation:
```bash
fluxui Test.flux
```

## Examples

### Simple Calculator
```flux
APP "Calculator" 300 400

VAR display = "0"

FRAME main {
    TEXTBOX display_box {
        TEXT: display
        WIDTH: 260
        HEIGHT: 40
        X: 10
        Y: 10
    }
    
    ROW button_row {
        BUTTON btn1 { TEXT: "1" ONCLICK: { append_digit("1") } }
        BUTTON btn2 { TEXT: "2" ONCLICK: { append_digit("2") } }
        BUTTON btn3 { TEXT: "3" ONCLICK: { append_digit("3") } }
    }
}

FUNC append_digit(digit) {
    SET display = display + digit
    SET_TEXT display_box display
}
```

### Data Visualization
```flux
APP "Data Viz" 800 600

LINE_PLOT sales_plot {
    WIDTH: 400
    HEIGHT: 300
    TITLE: "Sales Trend"
    DATA: [
        [1, 100], [2, 150], [3, 120],
        [4, 200], [5, 180], [6, 250]
    ]
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `fluxui Test.flux`
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

- **Issues:** Report on [GitHub Issues](https://github.com/zerogravitygamingx211-hash/FluxUI/issues)
- **Documentation:** See complete guides in packages
- **Community:** Join discussions on GitHub

---

**FluxUI v1.0.0** - Modern UI Programming Language  
**Platform:** Windows & Linux  
**License:** MIT License

## Support

For issues and questions:
1. Check the language reference documentation
2. Run the test file to verify functionality
3. Review examples in `Test.flux`

---

**FluxUI Version 1.0** - Modern UI Programming Made Simple
