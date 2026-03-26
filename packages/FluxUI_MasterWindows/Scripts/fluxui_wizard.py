#!/usr/bin/env python3
"""
FluxUI Complete Installation Wizard
Automated installer for FluxUI Programming Language
Handles: Installation, PATH, IDE, file associations, executables
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
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk

class FluxUIWizard:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("FluxUI Programming Language - Setup Wizard")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Installation settings
        self.install_path = os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "FluxUI")
        self.create_desktop_shortcut = True
        self.create_start_menu = True
        self.add_to_path = True
        self.associate_files = True
        self.install_ide = True
        self.create_executables = True
        self.install_samples = True
        
        # Installation steps
        self.current_step = 0
        self.total_steps = 5
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the wizard UI"""
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        self.setup_header(main_frame)
        
        # Content area
        self.content_frame = ctk.CTkFrame(main_frame)
        self.content_frame.pack(fill="both", expand=True, pady=(10, 0))
        
        # Navigation buttons
        self.setup_navigation(main_frame)
        
        # Show welcome screen
        self.show_welcome_screen()
        
    def setup_header(self, parent):
        """Setup header with logo and progress"""
        header_frame = ctk.CTkFrame(parent, height=100)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Logo and title
        logo_frame = ctk.CTkFrame(header_frame, width=80, height=80)
        logo_frame.pack(side="left", padx=10, pady=10)
        logo_frame.pack_propagate(False)
        
        logo_label = ctk.CTkLabel(logo_frame, text="⚡", font=ctk.CTkFont(size=40))
        logo_label.pack(expand=True)
        
        title_frame = ctk.CTkFrame(header_frame)
        title_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        title_label = ctk.CTkLabel(title_frame, text="FluxUI Programming Language", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(anchor="w", pady=(5, 0))
        
        subtitle_label = ctk.CTkLabel(title_frame, text="Complete Installation Wizard", 
                                     font=ctk.CTkFont(size=14), text_color="#888")
        subtitle_label.pack(anchor="w")
        
        desc_label = ctk.CTkLabel(title_frame, text="Modern UI Programming Made Simple", 
                                  font=ctk.CTkFont(size=12), text_color="#aaa")
        desc_label.pack(anchor="w")
        
        # Progress indicator
        progress_frame = ctk.CTkFrame(header_frame, width=200)
        progress_frame.pack(side="right", padx=10, pady=10)
        progress_frame.pack_propagate(False)
        
        self.step_label = ctk.CTkLabel(progress_frame, text=f"Step {self.current_step + 1} of {self.total_steps}")
        self.step_label.pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=180)
        self.progress_bar.pack(pady=5)
        self.update_progress()
        
    def setup_navigation(self, parent):
        """Setup navigation buttons"""
        nav_frame = ctk.CTkFrame(parent, height=70)
        nav_frame.pack(fill="x", pady=(10, 0))
        nav_frame.pack_propagate(False)
        
        # Back button
        self.back_button = ctk.CTkButton(nav_frame, text="← Back", width=100, 
                                        command=self.back_step, state="disabled")
        self.back_button.pack(side="left", padx=10, pady=15)
        
        # Next/Install button
        self.next_button = ctk.CTkButton(nav_frame, text="Next →", width=120,
                                        command=self.next_step)
        self.next_button.pack(side="right", padx=10, pady=15)
        
        # Cancel button
        cancel_button = ctk.CTkButton(nav_frame, text="Cancel", width=100,
                                     command=self.cancel_install)
        cancel_button.pack(side="right", padx=10, pady=15)
        
    def update_progress(self):
        """Update progress bar"""
        progress = (self.current_step + 1) / self.total_steps
        self.progress_bar.set(progress)
        self.step_label.configure(text=f"Step {self.current_step + 1} of {self.total_steps}")
        
    def clear_content(self):
        """Clear content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
    def show_welcome_screen(self):
        """Show welcome screen"""
        self.clear_content()
        
        welcome_frame = ctk.CTkFrame(self.content_frame)
        welcome_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Welcome title
        title_label = ctk.CTkLabel(welcome_frame, text="Welcome to FluxUI Setup",
                                  font=ctk.CTkFont(size=22, weight="bold"))
        title_label.pack(pady=(20, 10))
        
        # Description
        desc_text = """FluxUI is a modern programming language designed for creating beautiful user interfaces with ease.

This wizard will automatically install and configure:
• FluxUI Programming Language (FluxUI.exe)
• FluxUI Integrated Development Environment
• System PATH configuration
• .flux file associations
• Desktop shortcuts and Start Menu
• Sample projects and documentation

Click Next to continue with the installation."""
        
        desc_label = ctk.CTkLabel(welcome_frame, text=desc_text, justify="left")
        desc_label.pack(pady=10, padx=20)
        
        # Features list
        features_frame = ctk.CTkFrame(welcome_frame)
        features_frame.pack(fill="x", pady=20, padx=20)
        
        features_title = ctk.CTkLabel(features_frame, text="Key Features:",
                                     font=ctk.CTkFont(size=16, weight="bold"))
        features_title.pack(anchor="w", padx=10, pady=(10, 5))
        
        features = [
            "✓ Simple, readable syntax",
            "✓ Rich UI component library", 
            "✓ Event-driven programming",
            "✓ Built-in graphics and charts",
            "✓ Cross-platform support",
            "✓ Modern IDE with syntax highlighting",
            "✓ Global command-line tools",
            "✓ Automatic file associations"
        ]
        
        for feature in features:
            feature_label = ctk.CTkLabel(features_frame, text=feature, anchor="w")
            feature_label.pack(fill="x", padx=20, pady=2)
        
    def show_license_screen(self):
        """Show license screen"""
        self.clear_content()
        
        license_frame = ctk.CTkFrame(self.content_frame)
        license_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(license_frame, text="License Agreement",
                                  font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(20, 10))
        
        # License text
        license_text = """MIT License

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

FluxUI End User License Agreement (EULA)

By installing or using FluxUI, you agree to the following terms:

1. Usage
You are free to use, modify, and distribute FluxUI for personal or commercial purposes.

2. No Warranty
FluxUI is provided "as is", without any guarantees. The developer is not responsible for any damage, data loss, or issues caused by using this software.

3. Liability
The creator of FluxUI (ZeroGravityGamingX211) is not liable for any direct or indirect damages arising from the use of this software.

4. Modifications
You may modify the source code, but you must include the original license in any distributed version.

5. Redistribution
You are allowed to share FluxUI, but you must not misrepresent it as your own original work.

6. Termination
If you violate these terms, your right to use FluxUI is automatically revoked.

7. Updates
FluxUI may change over time. Continued use means you accept updated terms.

---

Project Repository:
https://github.com/zerogravitygamingx211-hash/FluxUI

By installing FluxUI, you agree to the terms of this license."""
        
        # Scrollable text widget for license
        text_frame = ctk.CTkFrame(license_frame)
        text_frame.pack(fill="both", expand=True, pady=10, padx=20)
        
        license_textbox = tk.Text(text_frame, wrap="word", height=15,
                                 background="#2b2b2b", foreground="#d4d4d4",
                                 font=("Consolas", 10))
        license_textbox.pack(fill="both", expand=True, padx=5, pady=5)
        license_textbox.insert("1.0", license_text)
        license_textbox.config(state="disabled")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=license_textbox.yview)
        scrollbar.pack(side="right", fill="y")
        license_textbox.configure(yscrollcommand=scrollbar.set)
        
        # Accept checkbox
        self.accept_var = tk.BooleanVar(value=False)
        accept_checkbox = ctk.CTkCheckBox(license_frame, text="I accept the license agreement",
                                        variable=self.accept_var)
        accept_checkbox.pack(pady=10)
        
    def show_install_options_screen(self):
        """Show installation options screen"""
        self.clear_content()
        
        options_frame = ctk.CTkFrame(self.content_frame)
        options_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(options_frame, text="Installation Options",
                                  font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(20, 10))
        
        # Installation path
        path_frame = ctk.CTkFrame(options_frame)
        path_frame.pack(fill="x", pady=10, padx=20)
        
        path_label = ctk.CTkLabel(path_frame, text="Installation Folder:",
                                 font=ctk.CTkFont(weight="bold"))
        path_label.pack(anchor="w", pady=(5, 0))
        
        path_input_frame = ctk.CTkFrame(path_frame)
        path_input_frame.pack(fill="x", pady=5)
        
        self.path_entry = ctk.CTkEntry(path_input_frame)
        self.path_entry.pack(side="left", fill="x", expand=True)
        self.path_entry.insert(0, self.install_path)
        
        browse_button = ctk.CTkButton(path_input_frame, text="Browse...", width=80,
                                      command=self.browse_install_path)
        browse_button.pack(side="right", padx=(5, 0))
        
        # Installation options
        options_list_frame = ctk.CTkFrame(options_frame)
        options_list_frame.pack(fill="both", expand=True, pady=10, padx=20)
        
        options_title = ctk.CTkLabel(options_list_frame, text="Select components to install:",
                                    font=ctk.CTkFont(weight="bold"))
        options_title.pack(anchor="w", pady=(10, 5))
        
        # Options checkboxes
        self.options_vars = {}
        
        options = [
            ("Create FluxUI.exe executable", "create_executables", True, "Main FluxUI interpreter"),
            ("Install FluxUI IDE", "install_ide", True, "Integrated Development Environment"),
            ("Add to system PATH", "add_to_path", True, "Global command-line access"),
            ("Associate .flux files", "associate_files", True, "Open .flux files with FluxUI.exe"),
            ("Create desktop shortcut", "desktop_shortcut", True, "Desktop shortcut for IDE"),
            ("Create Start Menu entry", "start_menu", True, "Start Menu shortcut"),
            ("Install sample projects", "install_samples", True, "Example projects and templates")
        ]
        
        for display_text, key, default, description in options:
            var = tk.BooleanVar(value=default)
            self.options_vars[key] = var
            
            option_frame = ctk.CTkFrame(options_list_frame)
            option_frame.pack(fill="x", pady=2)
            
            checkbox = ctk.CTkCheckBox(option_frame, text=display_text, variable=var)
            checkbox.pack(anchor="w")
            
            desc_label = ctk.CTkLabel(option_frame, text=description, font=ctk.CTkFont(size=10), text_color="#888")
            desc_label.pack(anchor="w", padx=(25, 0))
        
    def show_installation_screen(self):
        """Show installation progress screen"""
        self.clear_content()
        
        install_frame = ctk.CTkFrame(self.content_frame)
        install_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(install_frame, text="Installing FluxUI...",
                                  font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(20, 10))
        
        # Progress details
        details_frame = ctk.CTkFrame(install_frame)
        details_frame.pack(fill="both", expand=True, pady=10, padx=20)
        
        self.progress_text = tk.Text(details_frame, height=12, wrap="word",
                                   background="#2b2b2b", foreground="#d4d4d4",
                                   font=("Consolas", 9), state="disabled")
        self.progress_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Overall progress bar
        progress_frame = ctk.CTkFrame(install_frame)
        progress_frame.pack(fill="x", pady=10, padx=20)
        
        progress_label = ctk.CTkLabel(progress_frame, text="Installation Progress:")
        progress_label.pack(anchor="w", pady=(5, 0))
        
        self.install_progress = ctk.CTkProgressBar(progress_frame)
        self.install_progress.pack(fill="x", pady=5)
        
        # Start installation in background
        self.root.after(100, self.start_installation)
        
    def show_completion_screen(self):
        """Show installation completion screen"""
        self.clear_content()
        
        completion_frame = ctk.CTkFrame(self.content_frame)
        completion_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title_label = ctk.CTkLabel(completion_frame, text="Installation Complete!",
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(20, 10))
        
        # Success message
        success_text = """FluxUI Programming Language has been successfully installed!

What's installed:
• FluxUI.exe - Main language interpreter
• Global command-line tools (fluxui, fluxui-cli, fluxui-ide)
• .flux file associations
• Desktop and Start Menu shortcuts
• Sample projects and documentation

You can now:
• Run 'fluxui --version' from command line
• Double-click .flux files to execute them
• Launch FluxUI IDE from desktop or Start Menu
• Create new projects with 'fluxui new myapp'"""
        
        success_label = ctk.CTkLabel(completion_frame, text=success_text, justify="left")
        success_label.pack(pady=10, padx=20)
        
        # Options checkboxes
        options_frame = ctk.CTkFrame(completion_frame)
        options_frame.pack(fill="x", pady=20, padx=20)
        
        self.launch_ide_var = tk.BooleanVar(value=True)
        launch_checkbox = ctk.CTkCheckBox(options_frame, text="Launch FluxUI IDE",
                                        variable=self.launch_ide_var)
        launch_checkbox.pack(anchor="w", pady=5)
        
        self.open_samples_var = tk.BooleanVar(value=False)
        samples_checkbox = ctk.CTkCheckBox(options_frame, text="Open Sample Projects",
                                          variable=self.open_samples_var)
        samples_checkbox.pack(anchor="w", pady=5)
        
        self.view_docs_var = tk.BooleanVar(value=False)
        docs_checkbox = ctk.CTkCheckBox(options_frame, text="View Documentation",
                                      variable=self.view_docs_var)
        docs_checkbox.pack(anchor="w", pady=5)
        
        # Change next button to "Finish"
        self.next_button.configure(text="Finish", command=self.finish_installation)
        
    def browse_install_path(self):
        """Browse for installation path"""
        path = filedialog.askdirectory(title="Select Installation Folder", initialdir=self.install_path)
        if path:
            self.install_path = path
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, path)
            
    def next_step(self):
        """Go to next step"""
        print(f"Current step: {self.current_step}")
        
        if self.current_step == 1 and not self.accept_var.get():
            messagebox.showerror("License Required", "You must accept the license agreement to continue.")
            return
            
        if self.current_step == 2:
            # Save installation options
            self.install_path = self.path_entry.get()
            for key, var in self.options_vars.items():
                setattr(self, key, var.get())
            print(f"Installation options saved. Path: {self.install_path}")
        
        self.current_step += 1
        print(f"Moving to step: {self.current_step}")
        self.update_progress()
        
        # Update navigation buttons
        self.back_button.configure(state="normal")
        
        # Show appropriate screen
        if self.current_step == 1:
            self.show_license_screen()
        elif self.current_step == 2:
            self.show_install_options_screen()
        elif self.current_step == 3:
            self.show_installation_screen()
            self.next_button.configure(state="disabled")
        elif self.current_step == 4:
            self.show_completion_screen()
            self.next_button.configure(state="normal", text="Finish")
        elif self.current_step >= 5:
            self.finish_installation()
            
    def back_step(self):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.update_progress()
            
            # Update navigation buttons
            if self.current_step == 0:
                self.back_button.configure(state="disabled")
            
            self.next_button.configure(state="normal", text="Next →")
            
            # Show appropriate screen
            if self.current_step == 0:
                self.show_welcome_screen()
            elif self.current_step == 1:
                self.show_license_screen()
            elif self.current_step == 2:
                self.show_install_options_screen()
                
    def start_installation(self):
        """Start the installation process"""
        def install():
            steps = [
                ("Creating installation directory...", self.create_install_dir),
                ("Installing FluxUI core files...", self.install_core_files),
                ("Creating FluxUI.exe executable...", self.create_executables),
                ("Installing FluxUI IDE...", self.install_ide),
                ("Setting up file associations...", self.setup_file_associations),
                ("Adding to system PATH...", self.add_to_path),
                ("Creating shortcuts...", self.create_shortcuts),
                ("Installing samples...", self.install_samples),
                ("Finalizing installation...", self.finalize_installation)
            ]
            
            for i, (description, func) in enumerate(steps):
                self.log_progress(description)
                try:
                    func()
                    time.sleep(0.5)  # Simulate work
                except Exception as e:
                    self.log_progress(f"Error: {e}")
                
                # Update progress
                progress = (i + 1) / len(steps)
                self.install_progress.set(progress)
                self.root.update()
            
            # Installation complete
            self.log_progress("Installation completed successfully!")
            self.root.after(1000, lambda: self.next_step())
        
        # Run installation in background thread
        thread = threading.Thread(target=install)
        thread.daemon = True
        thread.start()
        
    def log_progress(self, message):
        """Log progress message"""
        self.progress_text.config(state="normal")
        self.progress_text.insert("end", f"{message}\n")
        self.progress_text.see("end")
        self.progress_text.config(state="disabled")
        self.root.update()
        
    def create_install_dir(self):
        """Create installation directory"""
        try:
            os.makedirs(self.install_path, exist_ok=True)
            os.makedirs(os.path.join(self.install_path, "bin"), exist_ok=True)
            os.makedirs(os.path.join(self.install_path, "lib"), exist_ok=True)
            os.makedirs(os.path.join(self.install_path, "docs"), exist_ok=True)
            os.makedirs(os.path.join(self.install_path, "samples"), exist_ok=True)
            print(f"  Created installation directory: {self.install_path}")
        except Exception as e:
            print(f"  Error creating directory: {e}")
            raise
        
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
        
        # Copy the real FluxUI.exe if it exists
        if os.path.exists("dist_executables/FluxUI.exe"):
            shutil.copy2("dist_executables/FluxUI.exe", os.path.join(bin_dir, "FluxUI.exe"))
            print("  Copied real FluxUI.exe")
        elif os.path.exists("dist/FluxUI.exe"):
            shutil.copy2("dist/FluxUI.exe", os.path.join(bin_dir, "FluxUI.exe"))
            print("  Copied real FluxUI.exe")
        else:
            # Fallback: Create batch file wrapper
            exe_content = f'''@echo off
python "{lib_dir}\\fluxui.py" %*
'''
            
            exe_path = os.path.join(bin_dir, "FluxUI.exe")
            with open(exe_path, "w") as f:
                f.write(exe_content)
            print("  Created batch wrapper for FluxUI.exe")
        
        # Copy other executables if they exist
        exe_mappings = {
            "fluxui-cli.exe": "fluxui-cli.exe",
            "fluxui-ide.exe": "fluxui-ide.exe"
        }
        
        for source_exe, target_exe in exe_mappings.items():
            if os.path.exists(f"dist_executables/{source_exe}"):
                shutil.copy2(f"dist_executables/{source_exe}", os.path.join(bin_dir, target_exe))
                print(f"  Copied real {source_exe}")
            elif os.path.exists(f"dist/{source_exe}"):
                shutil.copy2(f"dist/{source_exe}", os.path.join(bin_dir, target_exe))
                print(f"  Copied real {source_exe}")
            else:
                # Fallback: Create batch file wrapper
                content = f'''@echo off
python "{lib_dir}\\{source_exe.replace('.exe', '.py')}" %*
'''
                exe_path = os.path.join(bin_dir, target_exe)
                with open(exe_path, "w") as f:
                    f.write(content)
                print(f"  Created batch wrapper for {target_exe}")
        
        # Create fluxui.exe (alias to FluxUI.exe)
        if os.path.exists(os.path.join(bin_dir, "FluxUI.exe")):
            shutil.copy2(os.path.join(bin_dir, "FluxUI.exe"), os.path.join(bin_dir, "fluxui.exe"))
            print("  Created fluxui.exe alias")
        
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
            
            print("  File associations configured")
            
        except Exception as e:
            print(f"  Warning: Could not set file associations: {e}")
            
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
                subprocess.run(["setx", "PATH", new_path], capture_output=True)
                print("  Added to system PATH")
            else:
                print("  Already in PATH")
            
            winreg.CloseKey(key)
            
        except Exception as e:
            print(f"  Warning: Could not update PATH: {e}")
            
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
                print("  Created desktop shortcut")
            
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
                print("  Created Start Menu shortcut")
                
        except Exception as e:
            print(f"  Warning: Could not create shortcuts: {e}")
            
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
        print("  Installed sample projects")
            
    def finalize_installation(self):
        """Finalize installation"""
        # Create configuration
        config = {
            "version": "Beta 1.0",
            "install_path": self.install_path,
            "global_install": True,
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
        
    def cancel_install(self):
        """Cancel installation"""
        if messagebox.askyesno("Cancel Setup", "Are you sure you want to cancel the installation?"):
            self.root.quit()
            
    def finish_installation(self):
        """Finish installation"""
        # Handle post-installation options
        if self.launch_ide_var.get():
            try:
                subprocess.Popen([os.path.join(self.install_path, "bin", "fluxui-ide.exe")])
            except:
                pass
                
        if self.open_samples_var.get():
            samples_dir = os.path.join(self.install_path, "samples")
            if os.path.exists(samples_dir):
                os.startfile(samples_dir)
                
        if self.view_docs_var.get():
            docs_file = os.path.join(self.install_path, "docs", "FluxUI_Language_Reference.md")
            if os.path.exists(docs_file):
                os.startfile(docs_file)
        
        self.root.quit()
        
    def run(self):
        """Run the wizard"""
        self.root.mainloop()


if __name__ == "__main__":
    wizard = FluxUIWizard()
    wizard.run()
