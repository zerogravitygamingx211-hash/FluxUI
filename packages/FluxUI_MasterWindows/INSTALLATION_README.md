# FluxUI Installation Guide

## 🚀 Quick Installation

### Option 1: Automatic Setup Wizard (Recommended)

1. **Run the setup wizard:**
   ```bash
   setup_fluxui.bat
   ```

2. **Follow the wizard steps:**
   - Welcome screen
   - License agreement
   - Installation options
   - Automatic installation
   - Completion

### Option 2: Manual Installation

1. **Run as Administrator:**
   ```bash
   install_global.bat
   ```

## 📦 What Gets Installed

### Core Components
- **FluxUI.exe** - Main language interpreter
- **fluxui-cli** - Modern command-line interface
- **fluxui-ide** - Integrated Development Environment

### System Integration
- **System PATH** - Global command access
- **File Associations** - .flux files open with FluxUI.exe
- **Desktop Shortcuts** - Quick access to IDE
- **Start Menu** - Program group in Start Menu

### Documentation & Samples
- **Language Reference** - Complete documentation
- **Sample Projects** - Example code and templates
- **Templates** - Project templates for quick start

## 🎯 After Installation

### Global Commands Available
```bash
# Run FluxUI programs
fluxui program.flux

# Modern CLI interface
fluxui-cli new myapp
fluxui-cli run program.flux
fluxui-cli --help

# Launch IDE
fluxui-ide
```

### File Associations
- **Double-click** .flux files to execute them
- **Right-click** .flux files for more options
- **Open with** FluxUI.exe by default

### IDE Features
- **Syntax highlighting** for FluxUI language
- **Project management** with file explorer
- **Integrated console** for output
- **Code templates** and snippets
- **Build and run** tools

## 🔧 Verification

### Check Installation
```bash
fluxui --version
fluxui-cli check-global
```

### Test with Sample
```bash
fluxui Test.flux
```

### Launch IDE
```bash
fluxui-ide
# Or double-click desktop shortcut
```

## 📁 Installation Directory

Default location: `C:\Program Files\FluxUI\`

```
FluxUI/
├── bin/
│   ├── FluxUI.exe          # Main executable
│   ├── fluxui.exe          # CLI alias
│   ├── fluxui-cli.exe      # CLI tools
│   └── fluxui-ide.exe      # IDE launcher
├── lib/                    # Core libraries
├── docs/                   # Documentation
├── samples/                # Sample projects
└── config/                 # Configuration
```

## 🛠️ Troubleshooting

### Installation Issues
- **Run as Administrator** - Required for system changes
- **Check Python** - Make sure Python is installed
- **Antivirus** - May block installation, temporarily disable

### PATH Issues
- **Restart terminal** - After installation
- **Restart system** - For full PATH refresh
- **Manual PATH** - Add `C:\Program Files\FluxUI\bin` to PATH

### File Associations
- **Run wizard again** - Use "Repair" option
- **Manual setup** - Use `install_global.bat`
- **Reset associations** - Use Windows default programs

## 🔄 Uninstallation

### Automatic Uninstall
```bash
# Run wizard with uninstall option
python fluxui_wizard.py --uninstall
```

### Manual Uninstall
1. **Remove installation directory**
2. **Remove from system PATH**
3. **Remove file associations**
4. **Delete shortcuts**

## 🎨 Customization

### Installation Options
- **Choose components** - Install only what you need
- **Custom path** - Install to different directory
- **Shortcuts** - Enable/disable desktop/start menu

### Configuration
- **Global config** - `%APPDATA%\FluxUI\config.json`
- **User settings** - IDE preferences
- **Templates** - Custom project templates

## 📞 Support

### Getting Help
- **Documentation** - `FluxUI_Language_Reference.md`
- **Samples** - Check `samples/` directory
- **CLI Help** - `fluxui-cli --help`
- **Doctor** - `fluxui-cli doctor`

### Community
- **GitHub** - https://github.com/zerogravitygamingx211-hash/FluxUI
- **Discord** - https://discord.gg/fluxui
- **Website** - https://fluxui-lang.org

---

**FluxUI Version Beta 1.0** - Complete Installation Package

Thank you for choosing FluxUI! 🚀
