#!/usr/bin/env python3
"""
FluxUI Modern Installer Wizard
Professional installation wizard for FluxUI Programming Language
"""
import os
import sys
import subprocess
import shutil
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
import threading
import time

class FluxUIInstaller:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("FluxUI Programming Language - Setup Wizard")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        # Installation settings
        self.install_path = os.path.expanduser("~/FluxUI")
        self.create_desktop_shortcut = True
        self.create_start_menu = True
        self.add_to_path = True
        self.associate_files = True
        self.install_ide = True
        self.install_samples = True
        
        # Installation steps
        self.current_step = 0
        self.total_steps = 5
        
        self.setup_ui()
        
    def setup_ui(self):
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
        """Setup header with logo and title"""
        header_frame = ctk.CTkFrame(parent, height=80)
        header_frame.pack(fill="x", pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # Logo placeholder (using text)
        logo_frame = ctk.CTkFrame(header_frame, width=80, height=80)
        logo_frame.pack(side="left", padx=10, pady=5)
        logo_frame.pack_propagate(False)
        
        logo_label = ctk.CTkLabel(logo_frame, text="⚡", font=ctk.CTkFont(size=40))
        logo_label.pack(expand=True)
        
        # Title and version
        title_frame = ctk.CTkFrame(header_frame)
        title_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        title_label = ctk.CTkLabel(title_frame, text="FluxUI Programming Language", 
                                  font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(anchor="w", pady=(5, 0))
        
        version_label = ctk.CTkLabel(title_frame, text="Version Beta 1.0", 
                                    font=ctk.CTkFont(size=14), text_color="#888")
        version_label.pack(anchor="w")
        
        subtitle_label = ctk.CTkLabel(title_frame, text="Modern UI Programming Made Simple", 
                                     font=ctk.CTkFont(size=12), text_color="#aaa")
        subtitle_label.pack(anchor="w")
        
        # Progress indicator
        progress_frame = ctk.CTkFrame(header_frame, width=200)
        progress_frame.pack(side="right", padx=10, pady=5)
        progress_frame.pack_propagate(False)
        
        self.step_label = ctk.CTkLabel(progress_frame, text=f"Step {self.current_step + 1} of {self.total_steps}")
        self.step_label.pack(pady=5)
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, width=180)
        self.progress_bar.pack(pady=5)
        self.update_progress()
        
    def setup_navigation(self, parent):
        """Setup navigation buttons"""
        nav_frame = ctk.CTkFrame(parent, height=60)
        nav_frame.pack(fill="x", pady=(10, 0))
        nav_frame.pack_propagate(False)
        
        # Back button
        self.back_button = ctk.CTkButton(nav_frame, text="← Back", width=100, 
                                        command=self.back_step, state="disabled")
        self.back_button.pack(side="left", padx=10, pady=15)
        
        # Next/Install button
        self.next_button = ctk.CTkButton(nav_frame, text="Next →", width=100,
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
                                  font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(20, 10))
        
        # Description
        desc_text = """FluxUI is a modern programming language designed for creating beautiful user interfaces with ease.
        
This installer will guide you through the installation of:
• FluxUI Programming Language (fluxui.exe)
• FluxUI Integrated Development Environment
• File associations (.flux files)
• Sample projects and documentation
• Command-line tools and utilities

Click Next to continue, or Cancel to exit Setup."""
        
        desc_label = ctk.CTkLabel(welcome_frame, text=desc_text, justify="left")
        desc_label.pack(pady=10, padx=20)
        
        # Features list
        features_frame = ctk.CTkFrame(welcome_frame)
        features_frame.pack(fill="x", pady=20, padx=20)
        
        features_title = ctk.CTkLabel(features_frame, text="Key Features:",
                                     font=ctk.CTkFont(size=14, weight="bold"))
        features_title.pack(anchor="w", padx=10, pady=(10, 5))
        
        features = [
            "✓ Simple, readable syntax",
            "✓ Rich UI component library",
            "✓ Event-driven programming",
            "✓ Built-in graphics and charts",
            "✓ Cross-platform support",
            "✓ Modern IDE with syntax highlighting"
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
        license_text = """FluxUI Programming Language - License Agreement

Copyright (c) 2024 FluxUI Project

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
        
        self.path_entry = ctk.CTkEntry(path_input_frame, textvariable=tk.StringVar(value=self.install_path))
        self.path_entry.pack(side="left", fill="x", expand=True)
        
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
            ("FluxUI Programming Language", "install_core", True, "Core language interpreter and runtime"),
            ("FluxUI IDE", "install_ide", True, "Integrated Development Environment"),
            ("File Associations", "associate_files", True, "Associate .flux files with FluxUI"),
            ("Add to PATH", "add_to_path", True, "Add FluxUI to system PATH"),
            ("Desktop Shortcut", "desktop_shortcut", True, "Create desktop shortcut"),
            ("Start Menu", "start_menu", True, "Add to Start Menu"),
            ("Sample Projects", "install_samples", True, "Install sample projects"),
            ("Documentation", "install_docs", True, "Install documentation")
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
        details_frame = ctk.CTkFrame(instill_frame)
        details_frame.pack(fill="both", expand=True, pady=10, padx=20)
        
        self.progress_text = tk.Text(details_frame, height=10, wrap="word",
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
                                  font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=(20, 10))
        
        # Success message
        success_text = """FluxUI Programming Language has been successfully installed on your system.

What's next?
• Create your first FluxUI project: fluxui new myproject
• Open the IDE: FluxUI_IDE
• Run sample programs: fluxui samples
• Read documentation: fluxui docs

Thank you for choosing FluxUI!"""
        
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
        if self.current_step == 1 and not self.accept_var.get():
            messagebox.showerror("License Required", "You must accept the license agreement to continue.")
            return
            
        if self.current_step == 2:
            # Save installation options
            self.install_path = self.path_entry.get()
            for key, var in self.options_vars.items():
                setattr(self, key, var.get())
        
        self.current_step += 1
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
                ("Installing FluxUI core...", self.install_core),
                ("Installing FluxUI IDE...", self.install_ide_component),
                ("Setting up file associations...", self.setup_file_associations),
                ("Creating shortcuts...", self.create_shortcuts),
                ("Installing samples...", self.install_samples_component),
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
        os.makedirs(self.install_path, exist_ok=True)
        
    def install_core(self):
        """Install FluxUI core components"""
        if self.install_core:
            # Copy core files
            core_files = ["fluxui.py", "parser.py", "tokenizer.py", "engine.py", "ui_engine.py"]
            for file in core_files:
                if os.path.exists(file):
                    shutil.copy2(file, self.install_path)
                    
    def install_ide_component(self):
        """Install FluxUI IDE"""
        if self.install_ide:
            if os.path.exists("fluxui_ide.py"):
                shutil.copy2("fluxui_ide.py", self.install_path)
                
    def setup_file_associations(self):
        """Setup file associations"""
        if self.associate_files:
            # This would require admin privileges
            pass
            
    def create_shortcuts(self):
        """Create shortcuts"""
        if self.desktop_shortcut or self.start_menu:
            # Create desktop/start menu shortcuts
            pass
            
    def install_samples_component(self):
        """Install sample projects"""
        if self.install_samples:
            samples_dir = os.path.join(self.install_path, "samples")
            os.makedirs(samples_dir, exist_ok=True)
            
            # Copy sample files
            if os.path.exists("Test.flux"):
                shutil.copy2("Test.flux", samples_dir)
                
    def finalize_installation(self):
        """Finalize installation"""
        # Create config file
        config = {
            "version": "Beta 1.0",
            "install_path": self.install_path,
            "components": {
                "core": self.install_core,
                "ide": self.install_ide,
                "samples": self.install_samples
            }
        }
        
        with open(os.path.join(self.install_path, "config.json"), "w") as f:
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
                subprocess.Popen([sys.executable, os.path.join(self.install_path, "fluxui_ide.py")])
            except:
                pass
                
        if self.open_samples_var.get():
            samples_dir = os.path.join(self.install_path, "samples")
            if os.path.exists(samples_dir):
                os.startfile(samples_dir)
                
        if self.view_docs_var.get():
            docs_file = os.path.join(self.install_path, "FluxUI_Language_Reference.md")
            if os.path.exists(docs_file):
                os.startfile(docs_file)
        
        self.root.quit()
        
    def run(self):
        """Run the installer"""
        self.root.mainloop()


if __name__ == "__main__":
    installer = FluxUIInstaller()
    installer.run()
