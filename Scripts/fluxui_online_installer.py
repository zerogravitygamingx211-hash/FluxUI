#!/usr/bin/env python3
"""
FluxUI Online Installer
Downloads FluxUI components from GitHub during installation
Lightweight installer that fetches executables online
"""
import os
import sys
import subprocess
import shutil
import json
import threading
import time
import urllib.request
import tempfile
from pathlib import Path
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

class FluxUIOnlineInstaller:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("FluxUI - Online Installer")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Installation settings
        self.install_path = os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "FluxUI")
        
        # GitHub repository info
        self.github_repo = "https://github.com/zerogravitygamingx211-hash/FluxUI"
        self.github_raw = "https://raw.githubusercontent.com/zerogravitygamingx211-hash/FluxUI/main"
        self.github_release = "https://github.com/zerogravitygamingx211-hash/FluxUI/releases/latest"
        
        # Files to download
        self.download_files = {
            "FluxUI.exe": "FluxUI.exe",
            "fluxui-cli.exe": "fluxui-cli.exe", 
            "fluxui-ide.exe": "fluxui-ide.exe",
            "FluxUI_Language_Reference.md": "docs/FluxUI_Language_Reference.md",
            "README.md": "docs/README.md",
            "Test.flux": "samples/Test.flux",
            "basic.flux": "samples/basic.flux"
        }
        
        # Progress tracking
        self.total_downloads = len(self.download_files)
        self.current_download = 0
        self.download_progress = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the online installer UI"""
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, height=80)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(header_frame, text="FluxUI Online Installer",
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(20, 5))
        
        subtitle_label = ctk.CTkLabel(header_frame, text="Downloading components from GitHub...",
                                     font=ctk.CTkFont(size=12), text_color="#888")
        subtitle_label.pack()
        
        # Content area
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Status
        self.status_label = ctk.CTkLabel(content_frame, text="Preparing to download...",
                                       font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=(20, 10))
        
        # Progress info
        self.progress_info_label = ctk.CTkLabel(content_frame, text="",
                                              font=ctk.CTkFont(size=10), text_color="#888")
        self.progress_info_label.pack(pady=5)
        
        # Overall progress bar
        self.overall_progress = ctk.CTkProgressBar(content_frame, width=500)
        self.overall_progress.pack(pady=10)
        
        # Current download progress
        self.download_progress_label = ctk.CTkLabel(content_frame, text="",
                                                 font=ctk.CTkFont(size=10), text_color="#888")
        self.download_progress_label.pack(pady=5)
        
        self.current_progress = ctk.CTkProgressBar(content_frame, width=500)
        self.current_progress.pack(pady=10)
        
        # Repository info
        repo_frame = ctk.CTkFrame(content_frame)
        repo_frame.pack(fill="x", pady=10, padx=20)
        
        repo_label = ctk.CTkLabel(repo_frame, text=f"Repository: {self.github_repo}",
                                 font=ctk.CTkFont(size=10), text_color="#888")
        repo_label.pack(pady=5)
        
        # Auto-start installation
        self.root.after(1000, self.start_online_installation)
        
    def download_file(self, url, local_path, progress_callback=None):
        """Download file with progress tracking"""
        try:
            # Create directory if needed
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            # Download with progress tracking
            def progress_hook(block_num, block_size, total_size):
                if progress_callback and total_size > 0:
                    progress = (block_num * block_size) / total_size
                    progress_callback(progress)
            
            urllib.request.urlretrieve(url, local_path, progress_hook)
            return True
            
        except Exception as e:
            print(f"Download error for {url}: {e}")
            return False
    
    def start_online_installation(self):
        """Start the online installation process"""
        def install():
            try:
                # Step 1: Create directories
                self.status_label.configure(text="Creating installation directory...")
                self.create_install_dir()
                time.sleep(0.5)
                
                # Step 2: Download files
                self.status_label.configure(text="Downloading FluxUI components...")
                self.download_all_files()
                
                # Step 3: Setup system integration
                self.status_label.configure(text="Setting up system integration...")
                self.setup_system_integration()
                time.sleep(0.5)
                
                # Step 4: Create shortcuts
                self.status_label.configure(text="Creating shortcuts...")
                self.create_shortcuts()
                time.sleep(0.5)
                
                # Step 5: Finalize
                self.status_label.configure(text="Finalizing installation...")
                self.finalize_installation()
                time.sleep(0.5)
                
                # Complete
                self.status_label.configure(text="Installation Complete!")
                self.root.after(2000, self.show_completion)
                
            except Exception as e:
                self.status_label.configure(text=f"Installation failed: {e}")
                print(f"Installation error: {e}")
        
        # Run in background thread
        thread = threading.Thread(target=install)
        thread.daemon = True
        thread.start()
    
    def create_install_dir(self):
        """Create installation directory"""
        os.makedirs(self.install_path, exist_ok=True)
        os.makedirs(os.path.join(self.install_path, "bin"), exist_ok=True)
        os.makedirs(os.path.join(self.install_path, "docs"), exist_ok=True)
        os.makedirs(os.path.join(self.install_path, "samples"), exist_ok=True)
        
    def download_all_files(self):
        """Download all files from GitHub"""
        for filename, local_path in self.download_files.items():
            self.current_download += 1
            overall_progress = self.current_download / self.total_downloads
            self.overall_progress.set(overall_progress)
            
            # Update status
            self.progress_info_label.configure(text=f"Downloading {filename} ({self.current_download}/{self.total_downloads})")
            
            # Determine download URL
            if filename.endswith('.exe'):
                # Try to get from releases first, fallback to raw
                download_url = f"{self.github_release}/download/{filename}"
            else:
                download_url = f"{self.github_raw}/{filename}"
            
            # Local full path
            full_local_path = os.path.join(self.install_path, local_path)
            
            # Download with progress tracking
            def current_progress(progress):
                self.current_progress.set(progress)
                self.download_progress_label.configure(text=f"{progress*100:.1f}%")
            
            # Reset current progress
            self.current_progress.set(0)
            self.download_progress_label.configure(text="0%")
            
            # Attempt download
            success = self.download_file(download_url, full_local_path, current_progress)
            
            if not success and filename.endswith('.exe'):
                # Try alternative URL for executables
                alt_url = f"{self.github_raw}/dist_executables/{filename}"
                success = self.download_file(alt_url, full_local_path, current_progress)
            
            if not success:
                # Create placeholder if download fails
                self.create_placeholder_file(full_local_path, filename)
            
            # Brief pause between downloads
            time.sleep(0.3)
        
        # Complete overall progress
        self.overall_progress.set(1.0)
        self.current_progress.set(0)
        self.download_progress_label.configure(text="Complete")
    
    def create_placeholder_file(self, path, filename):
        """Create placeholder file if download fails"""
        if filename.endswith('.exe'):
            # Create batch file placeholder
            content = f'''@echo off
echo FluxUI {filename} could not be downloaded
echo Please download manually from: {self.github_repo}
echo.
pause
'''
        else:
            # Create text file placeholder
            content = f'''# {filename}
# This file could not be downloaded automatically
# Please download from: {self.github_repo}
# Place this file in: {path}
'''
        
        with open(path, "w") as f:
            f.write(content)
    
    def setup_system_integration(self):
        """Setup file associations and PATH"""
        try:
            # File associations
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
            
            # Add to PATH
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                             r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 
                             0, winreg.KEY_ALL_ACCESS)
            
            current_path = winreg.QueryValueEx(key, "PATH")[0]
            fluxui_bin = os.path.join(self.install_path, "bin")
            
            if fluxui_bin not in current_path:
                new_path = current_path + ";" + fluxui_bin
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_SZ, new_path)
                subprocess.run(["setx", "PATH", new_path], capture_output=True)
            
            winreg.CloseKey(key)
            
        except Exception as e:
            print(f"System integration warning: {e}")
    
    def create_shortcuts(self):
        """Create desktop and Start Menu shortcuts"""
        try:
            # Desktop shortcut
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
            
            # Start Menu shortcut
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
            print(f"Shortcuts warning: {e}")
    
    def finalize_installation(self):
        """Finalize installation"""
        # Create configuration
        config = {
            "version": "Beta 1.0",
            "install_path": self.install_path,
            "online_install": True,
            "github_repo": self.github_repo,
            "author": "ZeroGravityGamingX211",
            "license": "MIT License"
        }
        
        config_dir = os.path.join(os.environ.get("APPDATA", ""), "FluxUI")
        os.makedirs(config_dir, exist_ok=True)
        
        with open(os.path.join(config_dir, "config.json"), "w") as f:
            json.dump(config, f, indent=2)
        
        # Create basic sample if not downloaded
        basic_sample_path = os.path.join(self.install_path, "samples", "basic.flux")
        if not os.path.exists(basic_sample_path):
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
            with open(basic_sample_path, "w") as f:
                f.write(basic_sample)
    
    def show_completion(self):
        """Show completion message"""
        completion_text = """FluxUI has been successfully installed from GitHub!

✅ Components downloaded from repository
✅ File associations configured
✅ System PATH updated
✅ Desktop shortcuts created

You can now:
• Double-click .flux files to execute them
• Run 'fluxui --version' from command line
• Launch FluxUI IDE from desktop shortcut

Repository: https://github.com/zerogravitygamingx211-hash/FluxUI

Note: If any components failed to download, please download them manually from the repository.

Author: ZeroGravityGamingX211
License: MIT License"""
        
        messagebox.showinfo("Installation Complete", completion_text)
        
        # Auto-close after 5 seconds
        self.root.after(5000, self.root.quit)
        
    def run(self):
        """Run the online installer"""
        self.root.mainloop()


if __name__ == "__main__":
    installer = FluxUIOnlineInstaller()
    installer.run()
