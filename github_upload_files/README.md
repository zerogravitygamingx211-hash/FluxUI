# FluxUI Programming Language

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
