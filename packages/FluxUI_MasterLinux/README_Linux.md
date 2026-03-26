# FluxUI Master Linux Package

## 📦 Linux Installation Package

This package contains everything you need to run FluxUI on Linux.

### **🚀 Quick Installation**

1. **Extract Package:**
   ```bash
   tar -xzf FluxUI_MasterLinux.tar.gz
   cd FluxUI_MasterLinux
   ```

2. **Install Dependencies:**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install python3 python3-pip python3-tk
   
   # CentOS/RHEL
   sudo yum install python3 python3-pip python3-tkinter
   
   # Arch Linux
   sudo pacman -S python python-pip tk
   ```

3. **Run Installer:**
   ```bash
   chmod +x install_global.sh
   sudo ./install_global.sh
   ```

### **📁 Package Contents**

#### **Installation Scripts**
- `install_global.sh` - Global installation script
- `fluxui-ide.desktop` - Desktop entry file

#### **Source Code**
- `Scripts/` - All Python source files
- `fluxui.py` - Main interpreter
- `fluxui_ide.py` - IDE application
- `parser.py` - Language parser
- And more...

#### **Documentation**
- `FluxUI_Instruction_Book.md` - Complete learning guide
- `FluxUI_Language_Reference.md` - Language reference
- `README.md` - Main documentation

#### **Examples**
- `Test.flux` - Example program
- `test_executable.flux` - Executable test

#### **Graphics**
- `icons/` - All icons and logos
- Multiple sizes (16x16 to 256x256)
- SVG and PNG formats for Linux

### **🔧 System Requirements**

- **Linux:** Ubuntu 18.04+, CentOS 7+, Arch Linux, or similar
- **Python:** 3.8 or higher
- **GUI:** X11 or Wayland display server
- **Permissions:** sudo/root for global installation
- **Disk Space:** ~100MB

### **📋 Installation Steps**

#### **Method 1: Global Installation (Recommended)**
```bash
# 1. Extract package
tar -xzf FluxUI_MasterLinux.tar.gz
cd FluxUI_MasterLinux

# 2. Make installer executable
chmod +x install_global.sh

# 3. Run with sudo
sudo ./install_global.sh

# 4. Test installation
fluxui --ver
```

#### **Method 2: Local Installation**
```bash
# 1. Extract to home directory
tar -xzf FluxUI_MasterLinux.tar.gz -d ~/

# 2. Add to PATH
echo 'export PATH="$HOME/FluxUI_MasterLinux/Scripts:$PATH"' >> ~/.bashrc
source ~/.bashrc

# 3. Test
python3 ~/FluxUI_MasterLinux/Scripts/fluxui.py --ver
```

#### **Method 3: Python Package Installation**
```bash
# 1. Install dependencies
pip3 install customtkinter

# 2. Run directly
cd Scripts
python3 fluxui.py Test.flux
```

### **🎯 After Installation**

#### **Test Installation:**
```bash
fluxui --ver
```
Should output: `FluxUI Beta 1.0`

#### **Run Programs:**
```bash
fluxui Test.flux
fluxui-ide
```

#### **Desktop Integration:**
```bash
# Install desktop entry
cp fluxui-ide.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications/
```

### **🐧 Linux Integration**

#### **System PATH:**
- Global installation adds `/usr/local/bin/fluxui`
- Symbolic links to main interpreter
- Available from any terminal

#### **Desktop Entry:**
- Application menu integration
- Icon support
- Proper MIME types for .flux files

#### **File Associations:**
```bash
# Associate .flux files with FluxUI
xdg-mime default fluxui.desktop application/x-flux
```

### **🛠️ Advanced Usage**

#### **Build from Source:**
```bash
cd Scripts
python3 build_all_executables.py
```

#### **Development Mode:**
```bash
cd Scripts
python3 fluxui_ide.py
```

#### **Create Desktop Shortcut:**
```bash
# Create desktop launcher
cat > ~/Desktop/FluxUI_IDE.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=FluxUI IDE
Comment=FluxUI Programming Language IDE
Exec=fluxui-ide
Icon=fluxui
Terminal=false
Categories=Development;IDE;
EOF
chmod +x ~/Desktop/FluxUI_IDE.desktop
```

### **🔧 Troubleshooting**

#### **Common Issues:**
- **"python3: command not found"** → Install Python 3
- **"No module named 'tkinter'"** → Install tkinter package
- **"Permission denied"** → Use sudo for global installation
- **"Display not found"** → Check X11/Wayland setup

#### **Dependencies Installation:**
```bash
# Ubuntu/Debian
sudo apt install python3-dev python3-pil python3-pil.imagetk

# CentOS/RHEL
sudo yum install python3-devel python3-pillow python3-tkinter

# Arch Linux
sudo pacman -S python python-pip tk python-pillow
```

#### **Uninstallation:**
```bash
# Remove global installation
sudo rm -rf /usr/local/bin/fluxui*
sudo rm -rf /usr/local/lib/fluxui
sudo rm -rf /opt/fluxui

# Remove desktop entry
rm ~/.local/share/applications/fluxui-ide.desktop
```

### **📚 Documentation**

- **FluxUI_Instruction_Book.md** - Complete guide
- **Scripts/README.md** - Source code documentation
- **icons/README.md** - Icon specifications

### **🌐 Online Resources**

- **GitHub:** https://github.com/zerogravitygamingx211-hash/FluxUI
- **Releases:** Latest executables and updates
- **Issues:** Report bugs and request features

### **🔧 Package Manager Installation (Future)**

```bash
# AUR (Arch Linux) - Coming Soon
yay -S fluxui

# Snap - Coming Soon
snap install fluxui

# Flatpak - Coming Soon
flatpak install com.fluxui.FluxUI
```

---

**FluxUI v1.0.0 - Linux Master Package**  
**Platform:** Linux x64  
**Size:** ~100MB  
**License:** MIT License
