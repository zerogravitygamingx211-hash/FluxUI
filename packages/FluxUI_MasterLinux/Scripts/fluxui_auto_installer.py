#!/usr/bin/env python3
"""
FluxUI Auto Installer
Automated installer that runs silently when double-clicked
Performs complete setup without user interaction
"""
import os
import sys
import subprocess
import shutil
import json
import threading
import time
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

class FluxUIAutoInstaller:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("FluxUI - Installing...")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        # Installation settings
        self.install_path = os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "FluxUI")
        
        # Auto-install all components
        self.create_executables = True
        self.install_ide = True
        self.add_to_path = True
        self.associate_files = True
        self.create_desktop_shortcut = True
        self.create_start_menu = True
        self.install_samples = True
        
        # Progress tracking
        self.total_steps = 8
        self.current_step = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup minimal UI for auto-install"""
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="FluxUI Programming Language",
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(20, 10))
        
        # Status
        self.status_label = ctk.CTkLabel(main_frame, text="Installing FluxUI...",
                                       font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=10)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(main_frame, width=400)
        self.progress_bar.pack(pady=10)
        
        # Details
        self.details_label = ctk.CTkLabel(main_frame, text="Preparing installation...",
                                         font=ctk.CTkFont(size=10), text_color="#888")
        self.details_label.pack(pady=10)
        
        # Auto-start installation
        self.root.after(1000, self.start_auto_installation)
        
    def update_progress(self, step_text):
        """Update progress"""
        self.current_step += 1
        progress = self.current_step / self.total_steps
        self.progress_bar.set(progress)
        self.details_label.configure(text=step_text)
        self.root.update()
        
    def start_auto_installation(self):
        """Start automatic installation"""
        def install():
            steps = [
                ("Creating installation directory...", self.create_install_dir),
                ("Installing core files...", self.install_core_files),
                ("Creating FluxUI.exe...", self.create_executables),
                ("Installing IDE...", self.install_ide),
                ("Setting up file associations...", self.setup_file_associations),
                ("Adding to system PATH...", self.add_to_path),
                ("Creating shortcuts...", self.create_shortcuts),
                ("Installing samples...", self.install_samples)
            ]
            
            for step_text, func in steps:
                self.update_progress(step_text)
                try:
                    func()
                    time.sleep(0.8)  # Brief pause for visual feedback
                except Exception as e:
                    print(f"Error in {step_text}: {e}")
            
            # Installation complete
            self.update_progress("Installation complete!")
            self.root.after(1500, self.show_completion)
        
        # Run in background thread
        thread = threading.Thread(target=install)
        thread.daemon = True
        thread.start()
        
    def create_install_dir(self):
        """Create installation directory"""
        os.makedirs(self.install_path, exist_ok=True)
        os.makedirs(os.path.join(self.install_path, "bin"), exist_ok=True)
        os.makedirs(os.path.join(self.install_path, "lib"), exist_ok=True)
        os.makedirs(os.path.join(self.install_path, "docs"), exist_ok=True)
        os.makedirs(os.path.join(self.install_path, "samples"), exist_ok=True)
        
    def install_core_files(self):
        """Install core FluxUI files"""
        core_files = [
            "fluxui.py", "parser.py", "tokenizer.py", "parser_ast.py",
            "engine.py", "ui_engine.py", "components.py", "renderer.py",
            "flux_runner.py", "fluxui_cli.py"
        ]
        
        lib_dir = os.path.join(self.install_path, "lib")
        for file in core_files:
            if os.path.exists(file):
                shutil.copy2(file, lib_dir)
                
    def create_executables(self):
        """Create FluxUI.exe executable"""
        if not self.create_executables:
            return
            
        bin_dir = os.path.join(self.install_path, "bin")
        lib_dir = os.path.join(self.install_path, "lib")
        
        # Create FluxUI.exe
        exe_content = f'''@echo off
python "{lib_dir}\\fluxui.py" %*
'''
        
        exe_path = os.path.join(bin_dir, "FluxUI.exe")
        with open(exe_path, "w") as f:
            f.write(exe_content)
        
        # Create fluxui.exe (alias)
        alias_path = os.path.join(bin_dir, "fluxui.exe")
        with open(alias_path, "w") as f:
            f.write(exe_content)
        
        # Create CLI executables
        cli_exes = ["fluxui-cli", "fluxui-ide"]
        for exe_name in cli_exes:
            content = f'''@echo off
python "{lib_dir}\\{exe_name}.py" %*
'''
            exe_path = os.path.join(bin_dir, f"{exe_name}.exe")
            with open(exe_path, "w") as f:
                f.write(content)
        
    def install_ide(self):
        """Install FluxUI IDE"""
        if not self.install_ide:
            return
            
        lib_dir = os.path.join(self.install_path, "lib")
        if os.path.exists("fluxui_ide.py"):
            shutil.copy2("fluxui_ide.py", lib_dir)
            
    def setup_file_associations(self):
        """Setup .flux file associations"""
        if not self.associate_files:
            return
            
        try:
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
            winreg.SetValue(key, None, winreg.REG_SZ, f"{self.install_path}\\bin\\FluxUI.exe,0")
            winreg.CloseKey(key)
            
            # Set open command
            key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "FluxUIFile\\shell\\open\\command")
            winreg.SetValue(key, None, winreg.REG_SZ, f'"{self.install_path}\\bin\\FluxUI.exe" "%1"')
            winreg.CloseKey(key)
            
        except Exception as e:
            print(f"Warning: Could not set file associations: {e}")
            
    def add_to_path(self):
        """Add to system PATH"""
        if not self.add_to_path:
            return
            
        try:
            import winreg
            
            # Get current PATH
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                             r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 
                             0, winreg.KEY_ALL_ACCESS)
            
            current_path = winreg.QueryValueEx(key, "PATH")[0]
            
            # Add FluxUI bin directory if not present
            fluxui_bin = os.path.join(self.install_path, "bin")
            if fluxui_bin not in current_path:
                new_path = current_path + ";" + fluxui_bin
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_SZ, new_path)
            
            winreg.CloseKey(key)
            
            # Notify system of environment change
            subprocess.run(["setx", "PATH", new_path], capture_output=True)
            
        except Exception as e:
            print(f"Warning: Could not update PATH: {e}")
            
    def create_shortcuts(self):
        """Create desktop and Start Menu shortcuts"""
        if not self.create_desktop_shortcut and not self.create_start_menu:
            return
            
        try:
            if self.create_desktop_shortcut:
                # Create desktop shortcut
                desktop_path = os.path.join(os.environ.get("PUBLIC", ""), "Desktop")
                shortcut_path = os.path.join(desktop_path, "FluxUI IDE.lnk")
                
                shortcut_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
$Shortcut.TargetPath = '{os.path.join(self.install_path, "bin", "fluxui-ide.exe")}'
$Shortcut.Description = "FluxUI Integrated Development Environment"
$Shortcut.Save()
'''
                subprocess.run(["powershell", "-Command", shortcut_script], capture_output=True)
            
            if self.create_start_menu:
                # Create Start Menu shortcut
                start_menu_path = os.path.join(os.environ.get("APPDATA", ""), 
                                              "Microsoft\\Windows\\Start Menu\\Programs")
                shortcut_path = os.path.join(start_menu_path, "FluxUI IDE.lnk")
                
                shortcut_script = f'''
$WshShell = New-Object -comObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut('{shortcut_path}')
$Shortcut.TargetPath = '{os.path.join(self.install_path, "bin", "fluxui-ide.exe")}'
$Shortcut.Description = "FluxUI Integrated Development Environment"
$Shortcut.Save()
'''
                subprocess.run(["powershell", "-Command", shortcut_script], capture_output=True)
                
        except Exception as e:
            print(f"Warning: Could not create shortcuts: {e}")
            
    def install_samples(self):
        """Install sample projects"""
        if not self.install_samples:
            return
            
        samples_dir = os.path.join(self.install_path, "samples")
        
        # Copy sample files
        if os.path.exists("Test.flux"):
            shutil.copy2("Test.flux", samples_dir)
        
        if os.path.exists("test_executable.flux"):
            shutil.copy2("test_executable.flux", samples_dir)
            
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
        
        with open(os.path.join(samples_dir, "basic.flux"), "w") as f:
            f.write(basic_sample)
        
        # Copy documentation
        docs_dir = os.path.join(self.install_path, "docs")
        if os.path.exists("FluxUI_Language_Reference.md"):
            shutil.copy2("FluxUI_Language_Reference.md", docs_dir)
        if os.path.exists("README.md"):
            shutil.copy2("README.md", docs_dir)
            
    def show_completion(self):
        """Show completion message"""
        # Update UI
        self.status_label.configure(text="Installation Complete!")
        self.details_label.configure(text="FluxUI has been successfully installed")
        
        # Create configuration
        config = {
            "version": "Beta 1.0",
            "install_path": self.install_path,
            "global_install": True,
            "author": "ZeroGravityGamingX211",
            "repository": "https://github.com/zerogravitygamingx211-hash/FluxUI",
            "license": "MIT License",
            "components": {
                "executables": self.create_executables,
                "ide": self.install_ide,
                "path": self.add_to_path,
                "associations": self.associate_files
            }
        }
        
        config_dir = os.path.join(os.environ.get("APPDATA", ""), "FluxUI")
        os.makedirs(config_dir, exist_ok=True)
        
        with open(os.path.join(config_dir, "config.json"), "w") as f:
            json.dump(config, f, indent=2)
        
        # Show completion dialog
        completion_text = """FluxUI has been successfully installed!

✅ FluxUI.exe - Main executable
✅ Global commands - fluxui, fluxui-cli, fluxui-ide
✅ File associations - .flux files open with FluxUI.exe
✅ Desktop shortcuts - Quick access to IDE
✅ System PATH - Global access from command line

You can now:
• Double-click .flux files to execute them
• Run 'fluxui --version' from command line
• Launch FluxUI IDE from desktop shortcut

Repository: https://github.com/zerogravitygamingx211-hash/FluxUI

Author: ZeroGravityGamingX211
License: MIT License"""
        
        messagebox.showinfo("Installation Complete", completion_text)
        
        # Auto-close after 5 seconds
        self.root.after(5000, self.root.quit)
        
    def run(self):
        """Run the auto installer"""
        self.root.mainloop()


if __name__ == "__main__":
    installer = FluxUIAutoInstaller()
    installer.run()
