# FluxUI Master Windows Package

## 📦 Windows Installation Package

This package contains everything you need to run FluxUI on Windows.

### **🚀 Quick Installation**

1. **Run Installer:**
   ```
   Double-click: FluxUI_Installer.exe
   Right-click → "Run as administrator"
   ```

2. **Alternative Installation:**
   ```
   Run: FluxUI_v1.0.0_Installer.bat
   ```

### **📁 Package Contents**

#### **Executables**
- `FluxUI_Installer.exe` - Main installer
- `FluxUI_Executables.zip` - All executables (extracted by installer)

#### **Installation Scripts**
- `FluxUI_v1.0.0_Installer.bat` - Versioned installer
- `Install_FluxUI.bat` - Simple installer
- `Install_FluxUI_Online.bat` - Online installer
- `build_release.bat` - Build script
- `install_global.bat` - Global installation
- `setup_fluxui.bat` - Setup script

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
- Windows .ico and .png formats

### **🔧 System Requirements**

- **Windows:** 7, 8, 10, or 11
- **Architecture:** 64-bit recommended
- **Python:** 3.8+ (for source code)
- **Admin Rights:** Required for installation
- **Disk Space:** ~200MB

### **📋 Installation Steps**

1. **Download** this package
2. **Extract** to a folder
3. **Run** `FluxUI_Installer.exe` as administrator
4. **Follow** the installation prompts
5. **Restart** Command Prompt
6. **Test** with `fluxui --ver`

### **🎯 After Installation**

#### **Test Installation:**
```cmd
fluxui --ver
```
Should output: `FluxUI Beta 1.0`

#### **Run Programs:**
```cmd
fluxui Test.flux
fluxui-ide
```

#### **File Associations:**
- Double-click `.flux` files to run them
- Right-click → "Open with FluxUI"

### **🖥️ Windows Integration**

- **Start Menu:** FluxUI shortcuts added
- **Desktop:** FluxUI shortcut created
- **PATH:** Global command-line access
- **File Types:** .flux files associated
- **Registry:** Proper Windows integration

### **🛠️ Advanced Usage**

#### **Build from Source:**
```cmd
cd Scripts
python build_all_executables.py
```

#### **Manual Installation:**
```cmd
cd Sh
install_global.bat
```

#### **IDE Development:**
```cmd
cd Scripts
python fluxui_ide.py
```

### **🔧 Troubleshooting**

#### **Common Issues:**
- **"fluxui not found"** → Restart Command Prompt
- **"Access denied"** → Run as administrator
- **"Python not found"** → Install Python 3.8+

#### **Uninstallation:**
1. Run: `C:\Program Files\FluxUI\uninstall.bat` (if available)
2. Or manually delete `C:\Program Files\FluxUI`
3. Remove from system PATH
4. Delete file associations

### **📚 Documentation**

- **FluxUI_Instruction_Book.md** - Complete guide
- **Scripts/README.md** - Source code documentation
- **icons/README.md** - Icon specifications

### **🌐 Online Resources**

- **GitHub:** https://github.com/zerogravitygamingx211-hash/FluxUI
- **Releases:** Latest executables and updates
- **Issues:** Report bugs and request features

---

**FluxUI v1.0.0 - Windows Master Package**  
**Platform:** Windows x64  
**Size:** ~200MB  
**License:** MIT License
