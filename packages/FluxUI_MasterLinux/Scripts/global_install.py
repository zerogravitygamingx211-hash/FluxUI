#!/usr/bin/env python3
"""
FluxUI Global Installer
Installs FluxUI system-wide for global access
"""
import os
import sys
import subprocess
import shutil
import json
from pathlib import Path
import platform

class FluxUIGlobalInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.version = "Beta 1.0"
        self.install_paths = self.get_install_paths()
        
    def get_install_paths(self):
        """Get system-specific installation paths"""
        if self.system == "windows":
            return {
                "bin": os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "FluxUI", "bin"),
                "lib": os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "FluxUI", "lib"),
                "share": os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "FluxUI", "share"),
                "docs": os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "FluxUI", "docs"),
                "config": os.path.join(os.environ.get("APPDATA", ""), "FluxUI"),
                "desktop": os.path.join(os.environ.get("PUBLIC", ""), "Desktop"),
                "start_menu": os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs")
            }
        elif self.system == "linux":
            return {
                "bin": "/usr/local/bin",
                "lib": "/usr/local/lib/fluxui",
                "share": "/usr/local/share/fluxui",
                "docs": "/usr/local/share/doc/fluxui",
                "config": os.path.expanduser("~/.config/fluxui"),
                "desktop": os.path.expanduser("~/.local/share/applications"),
                "start_menu": os.path.expanduser("~/.local/share/applications")
            }
        elif self.system == "darwin":  # macOS
            return {
                "bin": "/usr/local/bin",
                "lib": "/usr/local/lib/fluxui",
                "share": "/usr/local/share/fluxui",
                "docs": "/usr/local/share/doc/fluxui",
                "config": os.path.expanduser("~/.config/fluxui"),
                "desktop": os.path.expanduser("~/Applications"),
                "start_menu": os.path.expanduser("~/Applications")
            }
        else:
            raise OSError(f"Unsupported platform: {self.system}")
    
    def check_admin_privileges(self):
        """Check if running with admin privileges"""
        if self.system == "windows":
            try:
                import ctypes
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except:
                return False
        else:
            return os.geteuid() == 0
    
    def create_directories(self):
        """Create installation directories"""
        print("Creating installation directories...")
        
        for path_name, path in self.install_paths.items():
            if path_name not in ["desktop", "start_menu"]:
                os.makedirs(path, exist_ok=True)
                print(f"  Created: {path}")
    
    def install_executables(self):
        """Install FluxUI executables to system bin"""
        print("Installing executables...")
        
        bin_dir = self.install_paths["bin"]
        
        # Install main fluxui executable
        fluxui_exe = os.path.join(bin_dir, "fluxui")
        if self.system == "windows":
            fluxui_exe += ".exe"
        
        # Copy and create executable
        if os.path.exists("fluxui.py"):
            if self.system == "windows":
                # Create Windows batch file
                batch_content = f'''@echo off
python "{os.path.join(self.install_paths["lib"], "core", "fluxui.py")}" %*
'''
                with open(fluxui_exe, "w") as f:
                    f.write(batch_content)
            else:
                # Create Unix script
                script_content = f'''#!/bin/bash
python "{os.path.join(self.install_paths["lib"], "core", "fluxui.py")}" "$@"
'''
                with open(fluxui_exe, "w") as f:
                    f.write(script_content)
                os.chmod(fluxui_exe, 0o755)
            
            print(f"  Installed: {fluxui_exe}")
        
        # Install CLI
        fluxui_cli = os.path.join(bin_dir, "fluxui-cli")
        if self.system == "windows":
            fluxui_cli += ".exe"
        
        if os.path.exists("fluxui_cli.py"):
            if self.system == "windows":
                batch_content = f'''@echo off
python "{os.path.join(self.install_paths["lib"], "core", "fluxui_cli.py")}" %*
'''
                with open(fluxui_cli, "w") as f:
                    f.write(batch_content)
            else:
                script_content = f'''#!/bin/bash
python "{os.path.join(self.install_paths["lib"], "core", "fluxui_cli.py")}" "$@"
'''
                with open(fluxui_cli, "w") as f:
                    f.write(script_content)
                os.chmod(fluxui_cli, 0o755)
            
            print(f"  Installed: {fluxui_cli}")
        
        # Install IDE
        fluxui_ide = os.path.join(bin_dir, "fluxui-ide")
        if self.system == "windows":
            fluxui_ide += ".exe"
        
        if os.path.exists("fluxui_ide.py"):
            if self.system == "windows":
                batch_content = f'''@echo off
python "{os.path.join(self.install_paths["lib"], "core", "fluxui_ide.py")}" %*
'''
                with open(fluxui_ide, "w") as f:
                    f.write(batch_content)
            else:
                script_content = f'''#!/bin/bash
python "{os.path.join(self.install_paths["lib"], "core", "fluxui_ide.py")}" "$@"
'''
                with open(fluxui_ide, "w") as f:
                    f.write(script_content)
                os.chmod(fluxui_ide, 0o755)
            
            print(f"  Installed: {fluxui_ide}")
    
    def install_libraries(self):
        """Install FluxUI libraries"""
        print("Installing libraries...")
        
        lib_dir = self.install_paths["lib"]
        core_dir = os.path.join(lib_dir, "core")
        
        # Core library files
        core_files = [
            "fluxui.py", "fluxui_cli.py", "fluxui_ide.py", "parser.py", 
            "tokenizer.py", "parser_ast.py", "engine.py", "ui_engine.py",
            "components.py", "renderer.py", "flux_runner.py"
        ]
        
        for file in core_files:
            if os.path.exists(file):
                shutil.copy2(file, core_dir)
                print(f"  Installed: {file}")
    
    def install_documentation(self):
        """Install documentation"""
        print("Installing documentation...")
        
        docs_dir = self.install_paths["docs"]
        
        # Copy documentation files
        doc_files = [
            "FluxUI_Language_Reference.md", "README.md", "fluxui_ascii.txt"
        ]
        
        for file in doc_files:
            if os.path.exists(file):
                shutil.copy2(file, docs_dir)
                print(f"  Installed docs: {file}")
    
    def setup_file_associations(self):
        """Setup .flux file associations"""
        print("Setting up file associations...")
        
        if self.system == "windows":
            try:
                # Windows registry associations
                import winreg
                
                # Create .flux file type
                key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, ".flux")
                winreg.SetValue(key, None, winreg.REG_SZ, "FluxUIFile")
                winreg.CloseKey(key)
                
                # Create FluxUIFile handler
                key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "FluxUIFile")
                winreg.SetValue(key, None, winreg.REG_SZ, "FluxUI Source File")
                winreg.CloseKey(key)
                
                # Set default icon
                key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "FluxUIFile\\DefaultIcon")
                winreg.SetValue(key, None, winreg.REG_SZ, f"{self.install_paths['bin']}\\fluxui-ide.exe,0")
                winreg.CloseKey(key)
                
                # Set open command
                key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "FluxUIFile\\shell\\open\\command")
                winreg.SetValue(key, None, winreg.REG_SZ, f'"{self.install_paths["bin"]}\\fluxui-ide.exe" "%1"')
                winreg.CloseKey(key)
                
                print("  Windows file associations set")
                
            except ImportError:
                print("  Warning: Cannot set Windows registry associations (winreg not available)")
            except Exception as e:
                print(f"  Warning: Failed to set file associations: {e}")
                
        elif self.system == "linux":
            # Create MIME type
            mime_content = '''<?xml version="1.0"?>
<mime-info xmlns='http://www.freedesktop.org/standards/shared-mime-info'>
  <mime-type type="text/x-fluxui">
    <comment>FluxUI Source File</comment>
    <glob pattern="*.flux"/>
  </mime-type>
</mime-info>'''
            
            mime_dir = os.path.expanduser("~/.local/share/mime")
            os.makedirs(mime_dir, exist_ok=True)
            
            with open(os.path.join(mime_dir, "fluxui.xml"), "w") as f:
                f.write(mime_content)
            
            # Update MIME database
            subprocess.run(["update-mime-database", os.path.expanduser("~/.local/share/mime")], 
                         capture_output=True)
            
            print("  Linux MIME associations set")
    
    def create_shortcuts(self):
        """Create desktop shortcuts"""
        print("Creating shortcuts...")
        
        if self.system == "windows":
            # Create desktop shortcut
            desktop_path = self.install_paths["desktop"]
            shortcut_path = os.path.join(desktop_path, "FluxUI IDE.lnk")
            
            try:
                import pythoncom
                from win32com.shell import shell, shellcon
                
                shortcut = pythoncom.CoCreateInstance(
                    shell.CLSID_ShellLink,
                    None,
                    shell.CLSCTX_INPROC_SERVER,
                    shell.IID_IShellLink
                )
                
                shortcut.SetPath(os.path.join(self.install_paths["bin"], "fluxui-ide.exe"))
                shortcut.SetDescription("FluxUI Integrated Development Environment")
                shortcut.SetWorkingDirectory(self.install_paths["bin"])
                
                persist_file = shortcut.QueryInterface(shell.IPIDListFile)
                persist_file.Save(shortcut_path, 0)
                
                print(f"  Desktop shortcut: {shortcut_path}")
                
            except ImportError:
                print("  Warning: Cannot create Windows shortcuts (pywin32 not available)")
            
        elif self.system == "linux":
            # Create desktop entry
            desktop_entry = f'''[Desktop Entry]
Version=1.0
Type=Application
Name=FluxUI IDE
Comment=FluxUI Integrated Development Environment
Exec={self.install_paths["bin"]}/fluxui-ide
Icon={self.install_paths["share"]}/fluxui.svg
Terminal=false
Categories=Development;IDE;
Keywords=programming;language;ui;development;
StartupWMClass=FluxUI_IDE
'''
            
            applications_dir = self.install_paths["desktop"]
            os.makedirs(applications_dir, exist_ok=True)
            
            with open(os.path.join(applications_dir, "fluxui-ide.desktop"), "w") as f:
                f.write(desktop_entry)
            
            print(f"  Desktop entry: {applications_dir}/fluxui-ide.desktop")
    
    def update_path(self):
        """Update system PATH"""
        print("Updating system PATH...")
        
        if self.system == "windows":
            try:
                import winreg
                
                # Get current PATH
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                 r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 
                                 0, winreg.KEY_ALL_ACCESS)
                
                current_path = winreg.QueryValueEx(key, "PATH")[0]
                
                # Add FluxUI bin directory if not present
                fluxui_bin = self.install_paths["bin"]
                if fluxui_bin not in current_path:
                    new_path = current_path + ";" + fluxui_bin
                    winreg.SetValueEx(key, "PATH", 0, winreg.REG_SZ, new_path)
                    print("  Added to system PATH")
                else:
                    print("  Already in PATH")
                
                winreg.CloseKey(key)
                
                # Notify system of environment change
                subprocess.run(["setx", "PATH", new_path], capture_output=True)
                
            except Exception as e:
                print(f"  Warning: Could not update PATH: {e}")
                
        elif self.system in ["linux", "darwin"]:
            # Create profile script
            profile_script = f'''# FluxUI PATH addition
export PATH="{self.install_paths["bin"]}:$PATH"
'''
            
            # Add to shell profiles
            profiles = ["~/.bashrc", "~/.zshrc", "~/.profile"]
            
            for profile in profiles:
                profile_path = os.path.expanduser(profile)
                if os.path.exists(profile_path):
                    with open(profile_path, "r") as f:
                        content = f.read()
                    
                    if self.install_paths["bin"] not in content:
                        with open(profile_path, "a") as f:
                            f.write(f"\n{profile_script}")
                        print(f"  Added to {profile}")
    
    def create_config(self):
        """Create global configuration"""
        print("Creating global configuration...")
        
        config_dir = self.install_paths["config"]
        os.makedirs(config_dir, exist_ok=True)
        
        config = {
            "version": self.version,
            "install_path": self.install_paths["lib"],
            "bin_path": self.install_paths["bin"],
            "global_install": True,
            "system": self.system,
            "file_associations": True,
            "path_updated": True
        }
        
        config_file = os.path.join(config_dir, "config.json")
        with open(config_file, "w") as f:
            json.dump(config, f, indent=2)
        
        print(f"  Config: {config_file}")
    
    def verify_installation(self):
        """Verify installation"""
        print("Verifying installation...")
        
        # Test fluxui command
        try:
            result = subprocess.run(["fluxui", "--version"], 
                                 capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("  ✓ fluxui command working")
            else:
                print("  ✗ fluxui command failed")
        except:
            print("  ✗ fluxui command not found")
        
        # Test fluxui-cli command
        try:
            result = subprocess.run(["fluxui-cli", "--version"], 
                                 capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print("  ✓ fluxui-cli command working")
            else:
                print("  ✗ fluxui-cli command failed")
        except:
            print("  ✗ fluxui-cli command not found")
        
        # Check file associations
        if self.system == "windows":
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, ".flux")
                file_type = winreg.QueryValue(key, None)
                winreg.CloseKey(key)
                
                if file_type == "FluxUIFile":
                    print("  ✓ File associations working")
                else:
                    print("  ✗ File associations incorrect")
            except:
                print("  ✗ File associations not found")
    
    def install(self):
        """Perform global installation"""
        print(f"FluxUI Global Installer v{self.version}")
        print(f"System: {self.system}")
        print("=" * 50)
        
        # Check privileges
        if not self.check_admin_privileges():
            print("ERROR: Administrator privileges required for global installation")
            if self.system == "windows":
                print("Please run this script as Administrator")
            else:
                print("Please run this script with sudo")
            return False
        
        try:
            self.create_directories()
            self.install_libraries()
            self.install_executables()
            self.install_documentation()
            self.setup_file_associations()
            self.create_shortcuts()
            self.update_path()
            self.create_config()
            
            print("\n" + "=" * 50)
            print("Global installation completed!")
            print("=" * 50)
            
            print(f"Installation directory: {self.install_paths['lib']}")
            print(f"Executables: {self.install_paths['bin']}")
            print(f"Configuration: {self.install_paths['config']}")
            
            print("\nCommands now available globally:")
            print("  fluxui        - Run FluxUI programs")
            print("  fluxui-cli    - Modern CLI interface")
            print("  fluxui-ide    - Integrated Development Environment")
            
            print("\nFile associations:")
            print("  .flux files now open with FluxUI IDE")
            
            print("\nYou may need to restart your terminal or system")
            print("for PATH changes to take effect.")
            
            # Verify installation
            print("\nVerifying installation...")
            self.verify_installation()
            
            return True
            
        except Exception as e:
            print(f"Installation failed: {e}")
            return False
    
    def uninstall(self):
        """Uninstall FluxUI globally"""
        print("FluxUI Global Uninstaller")
        print("=" * 30)
        
        if not self.check_admin_privileges():
            print("ERROR: Administrator privileges required")
            return False
        
        try:
            # Remove executables
            bin_dir = self.install_paths["bin"]
            for exe in ["fluxui", "fluxui-cli", "fluxui-ide"]:
                if self.system == "windows":
                    exe += ".exe"
                
                exe_path = os.path.join(bin_dir, exe)
                if os.path.exists(exe_path):
                    os.remove(exe_path)
                    print(f"  Removed: {exe_path}")
            
            # Remove libraries
            lib_dir = self.install_paths["lib"]
            if os.path.exists(lib_dir):
                shutil.rmtree(lib_dir)
                print(f"  Removed: {lib_dir}")
            
            # Remove documentation
            docs_dir = self.install_paths["docs"]
            if os.path.exists(docs_dir):
                shutil.rmtree(docs_dir)
                print(f"  Removed: {docs_dir}")
            
            # Remove shortcuts
            if self.system == "windows":
                desktop_shortcut = os.path.join(self.install_paths["desktop"], "FluxUI IDE.lnk")
                if os.path.exists(desktop_shortcut):
                    os.remove(desktop_shortcut)
                    print(f"  Removed: {desktop_shortcut}")
            else:
                desktop_entry = os.path.join(self.install_paths["desktop"], "fluxui-ide.desktop")
                if os.path.exists(desktop_entry):
                    os.remove(desktop_entry)
                    print(f"  Removed: {desktop_entry}")
            
            # Remove config
            config_dir = self.install_paths["config"]
            if os.path.exists(config_dir):
                shutil.rmtree(config_dir)
                print(f"  Removed: {config_dir}")
            
            print("\nUninstallation completed!")
            print("You may need to restart your system for all changes to take effect.")
            
            return True
            
        except Exception as e:
            print(f"Uninstallation failed: {e}")
            return False


if __name__ == "__main__":
    installer = FluxUIGlobalInstaller()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--uninstall":
        installer.uninstall()
    else:
        installer.install()
