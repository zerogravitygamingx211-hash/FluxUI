#!/usr/bin/env python3
"""
FluxUI IDE - Integrated Development Environment for FluxUI Language
Features: Syntax highlighting, code completion, project wizard, integrated runner
"""
import os
import sys
import subprocess
import json
from pathlib import Path
from tkinter import filedialog, messagebox
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import re

class FluxUIIDE:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.root = ctk.CTk()
        self.root.title("FluxUI IDE")
        self.root.geometry("1200x800")
        
        self.current_file = None
        self.project_path = None
        
        # FluxUI keywords for syntax highlighting
        self.keywords = {
            'variables': ['VAR', 'SET', 'DEL', 'TYPEOF', 'INSTANCEOF'],
            'control_flow': ['IF', 'ELIF', 'ELSE', 'WHILE', 'FOR', 'BREAK', 'CONTINUE', 'RETURN'],
            'functions': ['FUNC', 'CALL'],
            'error_handling': ['TRY', 'CATCH', 'THROW', 'ASSERT'],
            'file_io': ['READ_FILE', 'WRITE_FILE', 'COPY', 'PASTE'],
            'ui_widgets': ['APP', 'BUTTON', 'LABEL', 'INPUT', 'TEXTBOX', 'SWITCH', 'SLIDER', 'PROGRESS', 'DROPDOWN'],
            'layout': ['FRAME', 'GRID', 'ROW', 'COLUMN', 'PANE'],
            'events': ['ONCLICK', 'ONCHANGE', 'ONKEY', 'ONFOCUS'],
            'graphics': ['LINE_PLOT', 'BAR_CHART', 'PIE_CHART'],
            'system': ['SYS_EXEC', 'SYS_OPEN', 'SYS_NOTIFY'],
            'builtins': ['PRINT', 'ALERT', 'LOG', 'TRUE', 'FALSE', 'NULL'],
            'operators': ['AND', 'OR', 'NOT', 'IS', 'IN']
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Menu bar
        self.setup_menu()
        
        # Main container
        main_container = ctk.CTkFrame(self.root)
        main_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Left panel - File explorer
        self.setup_file_explorer(main_container)
        
        # Center - Code editor
        self.setup_code_editor(main_container)
        
        # Right panel - Tools
        self.setup_tools_panel(main_container)
        
        # Bottom - Output/console
        self.setup_console(main_container)
        
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Project", command=self.new_project_wizard)
        file_menu.add_command(label="New File", command=self.new_file)
        file_menu.add_command(label="Open File", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)
        
        # Run menu
        run_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Run", menu=run_menu)
        run_menu.add_command(label="Run", command=self.run_code)
        run_menu.add_command(label="Run with GUI", command=self.run_code_gui)
        run_menu.add_command(label="Build Executable", command=self.build_executable)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Project Wizard", command=self.new_project_wizard)
        tools_menu.add_command(label="Language Reference", command=self.show_language_reference)
        
    def setup_file_explorer(self, parent):
        # File explorer frame
        file_frame = ctk.CTkFrame(parent, width=200)
        file_frame.pack(side="left", fill="y", padx=(0, 5))
        file_frame.pack_propagate(False)
        
        # File explorer title
        title_label = ctk.CTkLabel(file_frame, text="Project Files", font=ctk.CTkFont(size=14, weight="bold"))
        title_label.pack(pady=5)
        
        # File tree
        self.file_tree = ttk.Treeview(file_frame, height=20)
        self.file_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar for tree
        tree_scroll = ttk.Scrollbar(file_frame, orient="vertical", command=self.file_tree.yview)
        tree_scroll.pack(side="right", fill="y")
        self.file_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Bind double-click to open files
        self.file_tree.bind("<Double-1>", self.on_file_double_click)
        
    def setup_code_editor(self, parent):
        # Code editor frame
        editor_frame = ctk.CTkFrame(parent)
        editor_frame.pack(side="left", fill="both", expand=True, padx=5)
        
        # Editor toolbar
        toolbar = ctk.CTkFrame(editor_frame, height=40)
        toolbar.pack(fill="x", pady=(0, 5))
        toolbar.pack_propagate(False)
        
        # Toolbar buttons
        ctk.CTkButton(toolbar, text="New", width=60, command=self.new_file).pack(side="left", padx=2)
        ctk.CTkButton(toolbar, text="Open", width=60, command=self.open_file).pack(side="left", padx=2)
        ctk.CTkButton(toolbar, text="Save", width=60, command=self.save_file).pack(side="left", padx=2)
        ctk.CTkButton(toolbar, text="Run", width=60, command=self.run_code).pack(side="left", padx=2)
        
        # Line numbers and text editor
        editor_container = ctk.CTkFrame(editor_frame)
        editor_container.pack(fill="both", expand=True)
        
        # Line numbers
        self.line_numbers = tk.Text(editor_container, width=4, padx=3, takefocus=0,
                                   border=0, background="#2b2b2b", foreground="#888888",
                                   state="disabled", wrap="none")
        self.line_numbers.pack(side="left", fill="y")
        
        # Code editor with syntax highlighting
        self.code_editor = tk.Text(editor_container, wrap="none", undo=True,
                                  background="#1e1e1e", foreground="#d4d4d4",
                                  insertbackground="#ffffff", selectbackground="#264f78",
                                  font=("Consolas", 11), tabs=("1c"))
        self.code_editor.pack(side="left", fill="both", expand=True)
        
        # Scrollbars
        v_scroll = ttk.Scrollbar(editor_container, orient="vertical", command=self.code_editor.yview)
        v_scroll.pack(side="right", fill="y")
        h_scroll = ttk.Scrollbar(editor_container, orient="horizontal", command=self.code_editor.xview)
        h_scroll.pack(side="bottom", fill="x")
        
        self.code_editor.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
        
        # Configure text tags for syntax highlighting
        self.configure_syntax_highlighting()
        
        # Bind events
        self.code_editor.bind("<KeyRelease>", self.on_key_release)
        self.code_editor.bind("<Key>", self.on_key_press)
        self.code_editor.bind("<Button-1>", self.on_click)
        self.code_editor.bind("<<Paste>>", self.on_paste)
        
    def setup_tools_panel(self, parent):
        # Tools panel frame
        tools_frame = ctk.CTkFrame(parent, width=250)
        tools_frame.pack(side="right", fill="y", padx=(5, 0))
        tools_frame.pack_propagate(False)
        
        # Tools title
        title_label = ctk.CTkLabel(tools_frame, text="Tools", font=ctk.CTkFont(size=14, weight="bold"))
        title_label.pack(pady=5)
        
        # Project info
        info_frame = ctk.CTkFrame(tools_frame)
        info_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(info_frame, text="Project Info", font=ctk.CTkFont(weight="bold")).pack(pady=2)
        self.project_label = ctk.CTkLabel(info_frame, text="No project open", text_color="#888")
        self.project_label.pack(pady=2)
        
        # Quick actions
        actions_frame = ctk.CTkFrame(tools_frame)
        actions_frame.pack(fill="x", padx=5, pady=10)
        
        ctk.CTkLabel(actions_frame, text="Quick Actions", font=ctk.CTkFont(weight="bold")).pack(pady=2)
        ctk.CTkButton(actions_frame, text="New Project", command=self.new_project_wizard).pack(fill="x", pady=2)
        ctk.CTkButton(actions_frame, text="Run Code", command=self.run_code).pack(fill="x", pady=2)
        ctk.CTkButton(actions_frame, text="Build EXE", command=self.build_executable).pack(fill="x", pady=2)
        
        # Templates
        templates_frame = ctk.CTkFrame(tools_frame)
        templates_frame.pack(fill="x", padx=5, pady=10)
        
        ctk.CTkLabel(templates_frame, text="Code Templates", font=ctk.CTkFont(weight="bold")).pack(pady=2)
        ctk.CTkButton(templates_frame, text="Basic App", command=self.insert_basic_app).pack(fill="x", pady=2)
        ctk.CTkButton(templates_frame, text="Function", command=self.insert_function).pack(fill="x", pady=2)
        ctk.CTkButton(templates_frame, text="UI Window", command=self.insert_ui_window).pack(fill="x", pady=2)
        
    def setup_console(self, parent):
        # Console frame
        console_frame = ctk.CTkFrame(parent, height=200)
        console_frame.pack(fill="x", pady=(5, 0))
        console_frame.pack_propagate(False)
        
        # Console title
        title_label = ctk.CTkLabel(console_frame, text="Console Output", font=ctk.CTkFont(size=12, weight="bold"))
        title_label.pack(anchor="w", padx=5, pady=2)
        
        # Console text area
        self.console = tk.Text(console_frame, height=8, background="#1e1e1e", foreground="#d4d4d4",
                             font=("Consolas", 10), wrap="word", state="disabled")
        self.console.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Console scrollbar
        console_scroll = ttk.Scrollbar(console_frame, orient="vertical", command=self.console.yview)
        console_scroll.pack(side="right", fill="y")
        self.console.configure(yscrollcommand=console_scroll.set)
        
    def configure_syntax_highlighting(self):
        """Configure syntax highlighting colors"""
        # Keywords
        for category, keywords in self.keywords.items():
            color = self.get_category_color(category)
            for keyword in keywords:
                self.code_editor.tag_configure(keyword, foreground=color)
        
        # Strings
        self.code_editor.tag_configure("string", foreground="#ce9178")
        
        # Comments
        self.code_editor.tag_configure("comment", foreground="#6a9955")
        
        # Numbers
        self.code_editor.tag_configure("number", foreground="#b5cea8")
        
    def get_category_color(self, category):
        """Get color for keyword category"""
        colors = {
            'variables': "#569cd6",
            'control_flow': "#c586c0",
            'functions': "#dcdcaa",
            'error_handling': "#c586c0",
            'file_io': "#4ec9b0",
            'ui_widgets': "#4ec9b0",
            'layout': "#4ec9b0",
            'events': "#9cdcfe",
            'graphics': "#4ec9b0",
            'system': "#d16969",
            'builtins': "#dcdcaa",
            'operators': "#d4d4d4"
        }
        return colors.get(category, "#d4d4d4")
    
    def highlight_syntax(self):
        """Apply syntax highlighting to current text"""
        content = self.code_editor.get("1.0", "end-1c")
        
        # Remove all existing tags
        for tag in self.code_editor.tag_names():
            self.code_editor.tag_remove(tag, "1.0", "end")
        
        # Highlight strings
        string_pattern = r'"[^"]*"|\'[^\']*\''
        for match in re.finditer(string_pattern, content):
            start, end = match.span()
            start_pos = f"1.0+{start}c"
            end_pos = f"1.0+{end}c"
            self.code_editor.tag_add("string", start_pos, end_pos)
        
        # Highlight comments
        comment_pattern = r'#.*$'
        for match in re.finditer(comment_pattern, content, re.MULTILINE):
            start, end = match.span()
            start_pos = f"1.0+{start}c"
            end_pos = f"1.0+{end}c"
            self.code_editor.tag_add("comment", start_pos, end_pos)
        
        # Highlight numbers
        number_pattern = r'\b\d+\.?\d*\b'
        for match in re.finditer(number_pattern, content):
            start, end = match.span()
            start_pos = f"1.0+{start}c"
            end_pos = f"1.0+{end}c"
            self.code_editor.tag_add("number", start_pos, end_pos)
        
        # Highlight keywords
        for category, keywords in self.keywords.items():
            for keyword in keywords:
                pattern = rf'\b{keyword}\b'
                for match in re.finditer(pattern, content):
                    start, end = match.span()
                    start_pos = f"1.0+{start}c"
                    end_pos = f"1.0+{end}c"
                    self.code_editor.tag_add(keyword, start_pos, end_pos)
    
    def update_line_numbers(self):
        """Update line numbers"""
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", "end")
        
        # Count lines
        lines = self.code_editor.get("1.0", "end-1c").split("\n")
        line_count = len(lines)
        
        # Add line numbers
        for i in range(1, line_count + 1):
            self.line_numbers.insert("end", f"{i}\n")
        
        self.line_numbers.config(state="disabled")
    
    def on_key_release(self, event):
        """Handle key release events"""
        self.highlight_syntax()
        self.update_line_numbers()
    
    def on_key_press(self, event):
        """Handle key press events"""
        # Auto-indent
        if event.keysym == "Return":
            # Get current line
            current_line = self.code_editor.get("insert linestart", "insert lineend")
            indent = re.match(r'^(\s*)', current_line).group(1)
            
            # Add extra indent for blocks
            if current_line.rstrip().endswith("{"):
                indent += "    "
            
            self.code_editor.insert("insert", f"\n{indent}")
            return "break"
        
        # Update line numbers on any key press
        self.root.after(1, self.update_line_numbers)
    
    def on_click(self, event):
        """Handle mouse click events"""
        self.highlight_syntax()
    
    def on_paste(self, event):
        """Handle paste events"""
        self.root.after(1, self.highlight_syntax)
        self.root.after(1, self.update_line_numbers)
    
    def new_file(self):
        """Create new file"""
        if self.current_file:
            if not self.confirm_save():
                return
        
        self.current_file = None
        self.code_editor.delete("1.0", "end")
        self.update_title()
    
    def open_file(self):
        """Open file"""
        if self.current_file:
            if not self.confirm_save():
                return
        
        file_path = filedialog.askopenfilename(
            title="Open FluxUI File",
            filetypes=[("FluxUI Files", "*.flux"), ("All Files", "*.*")]
        )
        
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.code_editor.delete("1.0", "end")
            self.code_editor.insert("1.0", content)
            self.current_file = file_path
            self.update_title()
            self.highlight_syntax()
            self.update_line_numbers()
    
    def save_file(self):
        """Save current file"""
        if not self.current_file:
            return self.save_file_as()
        
        try:
            with open(self.current_file, 'w', encoding='utf-8') as f:
                f.write(self.code_editor.get("1.0", "end-1c"))
            self.log_message(f"File saved: {self.current_file}")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")
            return False
    
    def save_file_as(self):
        """Save file with new name"""
        file_path = filedialog.asksaveasfilename(
            title="Save FluxUI File",
            defaultextension=".flux",
            filetypes=[("FluxUI Files", "*.flux"), ("All Files", "*.*")]
        )
        
        if file_path:
            self.current_file = file_path
            return self.save_file()
        return False
    
    def confirm_save(self):
        """Confirm save before closing"""
        if messagebox.askyesno("Save Changes", "Do you want to save changes?"):
            return self.save_file()
        return True
    
    def update_title(self):
        """Update window title"""
        title = "FluxUI IDE"
        if self.current_file:
            title += f" - {os.path.basename(self.current_file)}"
        self.root.title(title)
    
    def run_code(self):
        """Run the current FluxUI code"""
        if not self.save_file():
            return
        
        try:
            # Clear console
            self.console.config(state="normal")
            self.console.delete("1.0", "end")
            self.console.insert("1.0", f"Running: {self.current_file}\n")
            self.console.insert("end", "-" * 50 + "\n")
            self.console.config(state="disabled")
            
            # Run fluxui
            result = subprocess.run(
                [sys.executable, "fluxui.py", self.current_file],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            # Show output
            self.console.config(state="normal")
            if result.stdout:
                self.console.insert("end", result.stdout)
            if result.stderr:
                self.console.insert("end", f"Error:\n{result.stderr}")
            self.console.insert("end", "-" * 50 + "\n")
            self.console.insert("end", f"Exit code: {result.returncode}\n")
            self.console.see("end")
            self.console.config(state="disabled")
            
        except Exception as e:
            self.log_message(f"Error running code: {e}")
    
    def run_code_gui(self):
        """Run code with GUI"""
        if not self.save_file():
            return
        
        try:
            # Run with GUI flag
            subprocess.Popen(
                [sys.executable, "fluxui.py", self.current_file, "--gui"],
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            self.log_message(f"Running with GUI: {self.current_file}")
        except Exception as e:
            self.log_message(f"Error running GUI: {e}")
    
    def build_executable(self):
        """Build executable from current project"""
        self.log_message("Building executable...")
        
        try:
            result = subprocess.run(
                [sys.executable, "build_exe.py"],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(os.path.abspath(__file__))
            )
            
            self.console.config(state="normal")
            self.console.insert("end", result.stdout)
            if result.stderr:
                self.console.insert("end", f"Error:\n{result.stderr}")
            self.console.config(state="disabled")
            
        except Exception as e:
            self.log_message(f"Error building executable: {e}")
    
    def log_message(self, message):
        """Log message to console"""
        self.console.config(state="normal")
        self.console.insert("end", f"{message}\n")
        self.console.see("end")
        self.console.config(state="disabled")
    
    def on_file_double_click(self, event):
        """Handle file double click in tree"""
        selection = self.file_tree.selection()
        if selection:
            item = self.file_tree.item(selection[0])
            file_path = item['values'][0] if item['values'] else None
            
            if file_path and os.path.isfile(file_path):
                self.current_file = file_path
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.code_editor.delete("1.0", "end")
                self.code_editor.insert("1.0", content)
                self.update_title()
                self.highlight_syntax()
                self.update_line_numbers()
    
    def new_project_wizard(self):
        """Show new project wizard"""
        wizard = ProjectWizard(self.root, self)
        wizard.show()
    
    def show_language_reference(self):
        """Show language reference"""
        ref_file = os.path.join(os.path.dirname(__file__), "FluxUI_Language_Reference.md")
        if os.path.exists(ref_file):
            os.startfile(ref_file)
        else:
            messagebox.showinfo("Info", "Language reference not found")
    
    def insert_basic_app(self):
        """Insert basic app template"""
        template = '''# Basic FluxUI Application
APP "My App" 400 300

VAR message = "Hello, FluxUI!"

LABEL title {
    TEXT: message
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
        self.code_editor.insert("insert", template)
        self.highlight_syntax()
    
    def insert_function(self):
        """Insert function template"""
        template = '''FUNC function_name(param1, param2) {
    # Function body
    RETURN param1 + param2
}
'''
        self.code_editor.insert("insert", template)
        self.highlight_syntax()
    
    def insert_ui_window(self):
        """Insert UI window template"""
        template = '''APP "Window Title" 800 600

FRAME main_frame {
    WIDTH: 780
    HEIGHT: 580
    PADDING: 10
    
    LABEL title {
        TEXT: "Window Title"
        FONT_SIZE: 20
        X: 10
        Y: 10
    }
}
'''
        self.code_editor.insert("insert", template)
        self.highlight_syntax()
    
    def undo(self):
        """Undo action"""
        self.code_editor.edit_undo()
    
    def redo(self):
        """Redo action"""
        self.code_editor.edit_redo()
    
    def cut(self):
        """Cut selected text"""
        self.code_editor.event_generate("<<Cut>>")
    
    def copy(self):
        """Copy selected text"""
        self.code_editor.event_generate("<<Copy>>")
    
    def paste(self):
        """Paste text"""
        self.code_editor.event_generate("<<Paste>>")
    
    def load_project_files(self, project_path):
        """Load project files into tree"""
        self.file_tree.delete(*self.file_tree.get_children())
        
        if project_path and os.path.exists(project_path):
            self.project_path = project_path
            self.project_label.configure(text=os.path.basename(project_path))
            
            # Add files to tree
            for root, dirs, files in os.walk(project_path):
                for file in files:
                    if file.endswith('.flux') or file in ['README.md', 'package.json']:
                        file_path = os.path.join(root, file)
                        rel_path = os.path.relpath(file_path, project_path)
                        self.file_tree.insert("", "end", text=rel_path, values=(file_path,))
        else:
            self.project_label.configure(text="No project open")
    
    def run(self):
        """Start the IDE"""
        self.root.mainloop()


class ProjectWizard:
    def __init__(self, parent, ide):
        self.parent = parent
        self.ide = ide
        self.window = None
        
    def show(self):
        """Show project wizard dialog"""
        self.window = ctk.CTkToplevel(self.parent)
        self.window.title("New FluxUI Project")
        self.window.geometry("500x400")
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Main container
        container = ctk.CTkFrame(self.window)
        container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(container, text="Create New FluxUI Project", 
                            font=ctk.CTkFont(size=18, weight="bold"))
        title.pack(pady=(0, 20))
        
        # Project name
        ctk.CTkLabel(container, text="Project Name:").pack(anchor="w")
        self.name_entry = ctk.CTkEntry(container, width=400)
        self.name_entry.pack(fill="x", pady=(0, 15))
        self.name_entry.insert(0, "MyFluxProject")
        
        # Project location
        ctk.CTkLabel(container, text="Project Location:").pack(anchor="w")
        location_frame = ctk.CTkFrame(container)
        location_frame.pack(fill="x", pady=(0, 15))
        
        self.location_entry = ctk.CTkEntry(location_frame, width=350)
        self.location_entry.pack(side="left", fill="x", expand=True)
        self.location_entry.insert(0, os.path.expanduser("~/Desktop"))
        
        ctk.CTkButton(location_frame, text="Browse", width=80,
                     command=self.browse_location).pack(side="right", padx=(5, 0))
        
        # Project type
        ctk.CTkLabel(container, text="Project Type:").pack(anchor="w")
        self.type_var = tk.StringVar(value="basic")
        
        types_frame = ctk.CTkFrame(container)
        types_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkRadioButton(types_frame, text="Basic Application", 
                          variable=self.type_var, value="basic").pack(anchor="w")
        ctk.CTkRadioButton(types_frame, text="UI Application", 
                          variable=self.type_var, value="ui").pack(anchor="w")
        ctk.CTkRadioButton(types_frame, text="Data Visualization", 
                          variable=self.type_var, value="data").pack(anchor="w")
        ctk.CTkRadioButton(types_frame, text="Empty Project", 
                          variable=self.type_var, value="empty").pack(anchor="w")
        
        # Include files
        ctk.CTkLabel(container, text="Include Files:").pack(anchor="w")
        
        include_frame = ctk.CTkFrame(container)
        include_frame.pack(fill="x", pady=(0, 20))
        
        self.include_main = tk.BooleanVar(value=True)
        self.include_readme = tk.BooleanVar(value=True)
        self.include_test = tk.BooleanVar(value=True)
        
        ctk.CTkCheckBox(include_frame, text="main.flux", 
                       variable=self.include_main).pack(anchor="w")
        ctk.CTkCheckBox(include_frame, text="README.md", 
                       variable=self.include_readme).pack(anchor="w")
        ctk.CTkCheckBox(include_frame, text="test.flux", 
                       variable=self.include_test).pack(anchor="w")
        
        # Buttons
        button_frame = ctk.CTkFrame(container)
        button_frame.pack(fill="x")
        
        ctk.CTkButton(button_frame, text="Create", command=self.create_project,
                     width=100).pack(side="right", padx=(5, 0))
        ctk.CTkButton(button_frame, text="Cancel", command=self.window.destroy,
                     width=100).pack(side="right")
    
    def browse_location(self):
        """Browse for project location"""
        location = filedialog.askdirectory(title="Select Project Location")
        if location:
            self.location_entry.delete(0, "end")
            self.location_entry.insert(0, location)
    
    def create_project(self):
        """Create the new project"""
        name = self.name_entry.get().strip()
        location = self.location_entry.get().strip()
        project_type = self.type_var.get()
        
        if not name:
            messagebox.showerror("Error", "Please enter a project name")
            return
        
        if not location:
            messagebox.showerror("Error", "Please select a project location")
            return
        
        # Create project directory
        project_path = os.path.join(location, name)
        try:
            os.makedirs(project_path, exist_ok=True)
            
            # Create files based on selections
            if self.include_main.get():
                self.create_main_file(project_path, project_type)
            
            if self.include_readme.get():
                self.create_readme_file(project_path, name, project_type)
            
            if self.include_test.get():
                self.create_test_file(project_path)
            
            # Load project in IDE
            self.ide.load_project_files(project_path)
            
            messagebox.showinfo("Success", f"Project '{name}' created successfully!")
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create project: {e}")
    
    def create_main_file(self, project_path, project_type):
        """Create main.flux file"""
        templates = {
            "basic": '''# Basic FluxUI Application
# Created with FluxUI IDE

APP "Basic App" 400 300

VAR greeting = "Hello, FluxUI!"

LABEL title {
    TEXT: greeting
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
        SET greeting = "Button was clicked!"
        SET_TEXT title greeting
    }
}
''',
            "ui": '''# FluxUI Application
# Created with FluxUI IDE

APP "UI Application" 800 600

VAR counter = 0

FRAME main_frame {
    WIDTH: 780
    HEIGHT: 580
    PADDING: 10
    
    LABEL title {
        TEXT: "UI Application"
        FONT_SIZE: 20
        X: 10
        Y: 10
    }
    
    ROW controls {
        Y: 50
        SPACING: 10
        
        BUTTON increment_btn {
            TEXT: "Increment"
            ONCLICK: {
                SET counter += 1
                SET_TEXT counter_label "Count: " + counter
            }
        }
        
        BUTTON decrement_btn {
            TEXT: "Decrement"
            ONCLICK: {
                SET counter -= 1
                SET_TEXT counter_label "Count: " + counter
            }
        }
        
        BUTTON reset_btn {
            TEXT: "Reset"
            ONCLICK: {
                SET counter = 0
                SET_TEXT counter_label "Count: 0"
            }
        }
    }
    
    LABEL counter_label {
        TEXT: "Count: 0"
        FONT_SIZE: 14
        X: 10
        Y: 100
    }
}
''',
            "data": '''# Data Visualization Application
# Created with FluxUI IDE

APP "Data Visualization" 1000 700

VAR sample_data = [
    ["Jan", 100], ["Feb", 150], ["Mar", 120],
    ["Apr", 200], ["May", 180], ["Jun", 250]
]

FRAME main_frame {
    WIDTH: 980
    HEIGHT: 680
    PADDING: 10
    
    LABEL title {
        TEXT: "Sales Data Visualization"
        FONT_SIZE: 20
        X: 10
        Y: 10
    }
    
    LINE_PLOT sales_chart {
        WIDTH: 450
        HEIGHT: 300
        TITLE: "Monthly Sales Trend"
        X_LABEL: "Month"
        Y_LABEL: "Sales ($)"
        X: 10
        Y: 50
        DATA: sample_data
    }
    
    BAR_CHART sales_bar {
        WIDTH: 450
        HEIGHT: 300
        TITLE: "Sales by Month"
        X: 500
        Y: 50
        CATEGORIES: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        VALUES: [100, 150, 120, 200, 180, 250]
    }
    
    BUTTON refresh_btn {
        TEXT: "Refresh Data"
        X: 10
        Y: 370
        ONCLICK: {
            PRINT "Data refreshed!"
        }
    }
}
''',
            "empty": '''# Empty FluxUI Project
# Created with FluxUI IDE

APP "Empty Project" 400 300

# Add your code here
PRINT "Hello, FluxUI!"
'''
        }
        
        content = templates.get(project_type, templates["empty"])
        
        with open(os.path.join(project_path, "main.flux"), 'w') as f:
            f.write(content)
    
    def create_readme_file(self, project_path, name, project_type):
        """Create README.md file"""
        content = f'''# {name}

A FluxUI {project_type} project created with FluxUI IDE.

## Getting Started

This project uses the FluxUI programming language. To run the application:

```bash
fluxui main.flux
```

For GUI mode:
```bash
fluxui main.flux --gui
```

## Project Structure

- `main.flux` - Main application file
- `README.md` - This file

## Learn More

- [FluxUI Language Reference](https://fluxui-lang.org)
- [GitHub Repository](https://github.com/zerogravitygamingx211-hash/FluxUI)
- [FluxUI Documentation](https://fluxui-lang.org/docs)

## Building

To build an executable:
```bash
python build_exe.py
```

## License

This project is open source.
'''
        
        with open(os.path.join(project_path, "README.md"), 'w') as f:
            f.write(content)
    
    def create_test_file(self, project_path):
        """Create test.flux file"""
        content = '''# Test file for FluxUI project
# Run with: fluxui test.flux

PRINT "=== Running Tests ==="

# Test basic functionality
VAR test_var = "test"
ASSERT test_var == "test", "Variable test failed"

# Test arithmetic
VAR result = 2 + 3
ASSERT result == 5, "Arithmetic test failed"

# Test functions
FUNC test_func() {
    RETURN "success"
}

VAR func_result = test_func()
ASSERT func_result == "success", "Function test failed"

PRINT "All tests passed!"
'''
        
        with open(os.path.join(project_path, "test.flux"), 'w') as f:
            f.write(content)


if __name__ == "__main__":
    ide = FluxUIIDE()
    ide.run()
