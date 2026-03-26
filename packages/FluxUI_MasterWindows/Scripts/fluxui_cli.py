#!/usr/bin/env python3
"""
FluxUI Modern CLI - Command Line Interface
Professional CLI with help system, package management, and tools
"""
import os
import sys
import argparse
import subprocess
import json
import shutil
from pathlib import Path
import textwrap

class FluxUICLI:
    def __init__(self):
        self.version = "Beta 1.0"
        self.config_dir = os.path.expanduser("~/.fluxui")
        self.config_file = os.path.join(self.config_dir, "config.json")
        
        # Ensure config directory exists
        os.makedirs(self.config_dir, exist_ok=True)
        
        # Load or create config
        self.config = self.load_config()
        
    def load_config(self):
        """Load configuration from file"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        # Default config
        return {
            "version": self.version,
            "install_path": os.path.expanduser("~/FluxUI"),
            "default_template": "basic",
            "author": "FluxUI Developer",
            "editor": "FluxUI_IDE"
        }
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def create_parser(self):
        """Create argument parser"""
        parser = argparse.ArgumentParser(
            prog="fluxui",
            description="FluxUI Programming Language - Modern CLI",
            epilog="Visit https://fluxui-lang.org for more information",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            add_help=False
        )
        
        # Global options
        parser.add_argument("-h", "--help", action="help", help="Show this help message")
        parser.add_argument("--version", action="version", version=f"FluxUI {self.version}")
        parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
        
        # Subcommands
        subparsers = parser.add_subparsers(dest="command", help="Available commands")
        
        # Project commands
        self.add_project_commands(subparsers)
        
        # Build commands
        self.add_build_commands(subparsers)
        
        # Package commands
        self.add_package_commands(subparsers)
        
        # Config commands
        self.add_config_commands(subparsers)
        
        # Utility commands
        self.add_utility_commands(subparsers)
        
        # Global installation commands
        self.add_install_commands(subparsers)
        
        return parser
    
    def add_project_commands(self, subparsers):
        """Add project management commands"""
        
        # new command
        new_parser = subparsers.add_parser(
            "new",
            help="Create a new FluxUI project",
            description="Create a new FluxUI project with templates"
        )
        new_parser.add_argument("name", help="Project name")
        new_parser.add_argument("-t", "--template", choices=["basic", "ui", "data", "empty"], 
                               default="basic", help="Project template")
        new_parser.add_argument("-p", "--path", help="Project path")
        new_parser.add_argument("--ide", action="store_true", help="Open in IDE after creation")
        
        # run command
        run_parser = subparsers.add_parser(
            "run",
            help="Run a FluxUI program",
            description="Execute a FluxUI program"
        )
        run_parser.add_argument("file", help="FluxUI file to run")
        run_parser.add_argument("--gui", action="store_true", help="Run with GUI")
        run_parser.add_argument("--debug", action="store_true", help="Debug mode")
        
        # test command
        test_parser = subparsers.add_parser(
            "test",
            help="Run tests",
            description="Run FluxUI tests"
        )
        test_parser.add_argument("path", nargs="?", default=".", help="Test path")
        test_parser.add_argument("--watch", action="store_true", help="Watch mode")
        
    def add_build_commands(self, subparsers):
        """Add build commands"""
        
        # build command
        build_parser = subparsers.add_parser(
            "build",
            help="Build FluxUI project",
            description="Build executable from FluxUI project"
        )
        build_parser.add_argument("path", nargs="?", default=".", help="Project path")
        build_parser.add_argument("-o", "--output", help="Output file")
        build_parser.add_argument("--release", action="store_true", help="Release build")
        
        # clean command
        clean_parser = subparsers.add_parser(
            "clean",
            help="Clean build artifacts",
            description="Clean build artifacts and temporary files"
        )
        clean_parser.add_argument("path", nargs="?", default=".", help="Path to clean")
        
    def add_package_commands(self, subparsers):
        """Add package management commands"""
        
        # install command
        install_parser = subparsers.add_parser(
            "install",
            help="Install FluxUI packages",
            description="Install packages and dependencies"
        )
        install_parser.add_argument("package", nargs="?", help="Package to install")
        install_parser.add_argument("--global", action="store_true", help="Install globally")
        
        # uninstall command
        uninstall_parser = subparsers.add_parser(
            "uninstall",
            help="Uninstall FluxUI packages",
            description="Uninstall packages"
        )
        uninstall_parser.add_argument("package", help="Package to uninstall")
        
        # list command
        list_parser = subparsers.add_parser(
            "list",
            help="List installed packages",
            description="List all installed packages"
        )
        list_parser.add_argument("--global", action="store_true", help="List global packages")
        
        # search command
        search_parser = subparsers.add_parser(
            "search",
            help="Search packages",
            description="Search for available packages"
        )
        search_parser.add_argument("query", help="Search query")
        
    def add_config_commands(self, subparsers):
        """Add configuration commands"""
        
        # config command
        config_parser = subparsers.add_parser(
            "config",
            help="Manage configuration",
            description="View and modify FluxUI configuration"
        )
        config_parser.add_argument("key", nargs="?", help="Configuration key")
        config_parser.add_argument("value", nargs="?", help="Configuration value")
        config_parser.add_argument("--list", action="store_true", help="List all configuration")
        config_parser.add_argument("--reset", action="store_true", help="Reset configuration")
        
        # init command
        init_parser = subparsers.add_parser(
            "init",
            help="Initialize FluxUI environment",
            description="Initialize FluxUI environment in current directory"
        )
        init_parser.add_argument("--force", action="store_true", help="Force initialization")
        
    def add_install_commands(self, subparsers):
        """Add global installation commands"""
        
        # install-global command
        install_parser = subparsers.add_parser(
            "install-global",
            help="Install FluxUI globally",
            description="Install FluxUI system-wide for global access"
        )
        install_parser.add_argument("--force", action="store_true", help="Force installation")
        install_parser.add_argument("--uninstall", action="store_true", help="Uninstall global installation")
        
        # check-global command
        check_parser = subparsers.add_parser(
            "check-global",
            help="Check global installation",
            description="Check if FluxUI is installed globally"
        )
    
    def add_utility_commands(self, subparsers):
        """Add utility commands"""
        
        # doctor command
        doctor_parser = subparsers.add_parser(
            "doctor",
            help="Check system health",
            description="Check FluxUI installation and dependencies"
        )
        
        # update command
        update_parser = subparsers.add_parser(
            "update",
            help="Update FluxUI",
            description="Update FluxUI to latest version"
        )
        update_parser.add_argument("--check", action="store_true", help="Check for updates only")
        
        # docs command
        docs_parser = subparsers.add_parser(
            "docs",
            help="Open documentation",
            description="Open FluxUI documentation"
        )
        docs_parser.add_argument("topic", nargs="?", help="Documentation topic")
        
        # samples command
        samples_parser = subparsers.add_parser(
            "samples",
            help="Manage sample projects",
            description="List and create sample projects"
        )
        samples_parser.add_argument("name", nargs="?", help="Sample name")
        samples_parser.add_argument("--create", action="store_true", help="Create sample project")
        samples_parser.add_argument("--list", action="store_true", help="List available samples")
        
    def handle_command(self, args):
        """Handle command execution"""
        if args.command == "new":
            self.cmd_new(args)
        elif args.command == "run":
            self.cmd_run(args)
        elif args.command == "test":
            self.cmd_test(args)
        elif args.command == "build":
            self.cmd_build(args)
        elif args.command == "clean":
            self.cmd_clean(args)
        elif args.command == "install":
            self.cmd_install(args)
        elif args.command == "uninstall":
            self.cmd_uninstall(args)
        elif args.command == "list":
            self.cmd_list(args)
        elif args.command == "search":
            self.cmd_search(args)
        elif args.command == "config":
            self.cmd_config(args)
        elif args.command == "init":
            self.cmd_init(args)
        elif args.command == "doctor":
            self.cmd_doctor()
        elif args.command == "update":
            self.cmd_update(args)
        elif args.command == "docs":
            self.cmd_docs(args)
        elif args.command == "samples":
            self.cmd_samples(args)
        elif args.command == "install-global":
            self.cmd_install_global(args)
        elif args.command == "check-global":
            self.cmd_check_global()
        else:
            self.show_help()
    
    def cmd_new(self, args):
        """Handle new command"""
        print(f"🚀 Creating new FluxUI project: {args.name}")
        
        # Determine project path
        if args.path:
            project_path = os.path.join(args.path, args.name)
        else:
            project_path = os.path.join(os.getcwd(), args.name)
        
        # Create project directory
        os.makedirs(project_path, exist_ok=True)
        
        # Create project structure
        self.create_project_structure(project_path, args.name, args.template)
        
        print(f"✅ Project '{args.name}' created at {project_path}")
        print(f"📁 Template: {args.template}")
        
        # Open in IDE if requested
        if args.ide:
            self.open_ide(project_path)
        
        print(f"🎯 Next steps:")
        print(f"   cd {args.name}")
        print(f"   fluxui run main.flux")
    
    def cmd_run(self, args):
        """Handle run command"""
        if not os.path.exists(args.file):
            print(f"❌ File not found: {args.file}")
            return
        
        print(f"🏃 Running {args.file}")
        
        # Build command
        cmd = [sys.executable, "fluxui.py", args.file]
        if args.gui:
            cmd.append("--gui")
        if args.debug:
            cmd.append("--debug")
        
        # Run the program
        try:
            result = subprocess.run(cmd, capture_output=False)
            if result.returncode == 0:
                print("✅ Program executed successfully")
            else:
                print(f"❌ Program exited with code {result.returncode}")
        except Exception as e:
            print(f"❌ Error running program: {e}")
    
    def cmd_test(self, args):
        """Handle test command"""
        print(f"🧪 Running tests in {args.path}")
        
        # Find test files
        test_files = []
        for root, dirs, files in os.walk(args.path):
            for file in files:
                if file.endswith("_test.flux") or file == "test.flux":
                    test_files.append(os.path.join(root, file))
        
        if not test_files:
            print("ℹ️  No test files found")
            return
        
        # Run tests
        passed = 0
        failed = 0
        
        for test_file in test_files:
            print(f"🔍 Running {os.path.relpath(test_file, args.path)}")
            try:
                result = subprocess.run([sys.executable, "fluxui.py", test_file], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ PASSED")
                    passed += 1
                else:
                    print("❌ FAILED")
                    if args.verbose:
                        print(result.stderr)
                    failed += 1
            except Exception as e:
                print(f"❌ ERROR: {e}")
                failed += 1
        
        print(f"\n📊 Test Results: {passed} passed, {failed} failed")
        
        if args.watch:
            print("👀 Watching for changes... (Ctrl+C to stop)")
            # Implement watch mode here
    
    def cmd_build(self, args):
        """Handle build command"""
        print(f"🔨 Building project at {args.path}")
        
        # Find build script
        build_script = os.path.join(args.path, "build.flux")
        if not os.path.exists(build_script):
            # Use default build
            build_script = "build_exe.py"
        
        try:
            cmd = [sys.executable, build_script]
            if args.output:
                cmd.extend(["-o", args.output])
            if args.release:
                cmd.append("--release")
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Build successful")
                if result.stdout:
                    print(result.stdout)
            else:
                print("❌ Build failed")
                if result.stderr:
                    print(result.stderr)
        except Exception as e:
            print(f"❌ Build error: {e}")
    
    def cmd_clean(self, args):
        """Handle clean command"""
        print(f"🧹 Cleaning {args.path}")
        
        # Clean common build artifacts
        artifacts = [
            "build", "dist", "__pycache__", "*.pyc", 
            "*.exe", "*.zip", ".fluxui_build"
        ]
        
        cleaned = 0
        for artifact in artifacts:
            for path in Path(args.path).glob(artifact):
                if path.is_file():
                    path.unlink()
                    cleaned += 1
                elif path.is_dir():
                    shutil.rmtree(path)
                    cleaned += 1
        
        print(f"✅ Cleaned {cleaned} artifacts")
    
    def cmd_install(self, args):
        """Handle install command"""
        if args.package:
            print(f"📦 Installing package: {args.package}")
            # Implement package installation
        else:
            print("📦 Installing dependencies...")
            # Install default dependencies
    
    def cmd_uninstall(self, args):
        """Handle uninstall command"""
        print(f"🗑️  Uninstalling package: {args.package}")
        # Implement package uninstallation
    
    def cmd_list(self, args):
        """Handle list command"""
        print("📋 Installed packages:")
        # List installed packages
    
    def cmd_search(self, args):
        """Handle search command"""
        print(f"🔍 Searching for: {args.query}")
        # Search packages
    
    def cmd_config(self, args):
        """Handle config command"""
        if args.list:
            print("⚙️  Configuration:")
            for key, value in self.config.items():
                print(f"   {key}: {value}")
        elif args.reset:
            self.config = {}
            self.save_config()
            print("✅ Configuration reset")
        elif args.key and args.value:
            self.config[args.key] = args.value
            self.save_config()
            print(f"✅ Set {args.key} = {args.value}")
        elif args.key:
            value = self.config.get(args.key)
            if value:
                print(f"{args.key}: {value}")
            else:
                print(f"❌ Configuration key '{args.key}' not found")
        else:
            print("⚙️  FluxUI Configuration")
            print(f"   Version: {self.config.get('version', 'Unknown')}")
            print(f"   Install Path: {self.config.get('install_path', 'Unknown')}")
    
    def cmd_init(self, args):
        """Handle init command"""
        print("🚀 Initializing FluxUI environment")
        
        # Create .fluxui directory
        fluxui_dir = ".fluxui"
        if os.path.exists(fluxui_dir) and not args.force:
            print("❌ FluxUI environment already exists (use --force to override)")
            return
        
        os.makedirs(fluxui_dir, exist_ok=True)
        
        # Create project files
        self.create_project_files(".")
        
        print("✅ FluxUI environment initialized")
    
    def cmd_doctor(self):
        """Handle doctor command"""
        print("🩺 FluxUI System Check")
        
        checks = [
            ("Python", self.check_python),
            ("Dependencies", self.check_dependencies),
            ("Configuration", self.check_config),
            ("Installation", self.check_installation)
        ]
        
        all_good = True
        
        for name, check_func in checks:
            print(f"\n🔍 Checking {name}...")
            try:
                if check_func():
                    print(f"✅ {name} OK")
                else:
                    print(f"❌ {name} issues found")
                    all_good = False
            except Exception as e:
                print(f"❌ {name} check failed: {e}")
                all_good = False
        
        if all_good:
            print("\n🎉 Everything looks good!")
        else:
            print("\n⚠️  Some issues found. Please check the installation.")
    
    def cmd_update(self, args):
        """Handle update command"""
        if args.check:
            print("🔍 Checking for updates...")
            # Check for updates
        else:
            print("🔄 Updating FluxUI...")
            # Perform update
    
    def cmd_docs(self, args):
        """Handle docs command"""
        if args.topic:
            print(f"📚 Opening documentation for: {args.topic}")
            # Open specific documentation
        else:
            print("📚 Opening documentation...")
            # Open main documentation
    
    def cmd_samples(self, args):
        """Handle samples command"""
        if args.list:
            print("📋 Available samples:")
            samples = ["basic", "ui", "data", "game", "calculator"]
            for sample in samples:
                print(f"   {sample}")
        elif args.name and args.create:
            print(f"📁 Creating sample: {args.name}")
            # Create sample project
        elif args.name:
            print(f"📁 Sample: {args.name}")
            # Show sample details
        else:
            print("📁 FluxUI Samples")
            print("Use 'fluxui samples --list' to see available samples")
    
    def cmd_install_global(self, args):
        """Handle global installation command"""
        print("🌍 FluxUI Global Installation")
        print("=" * 40)
        
        if args.uninstall:
            print("Uninstalling FluxUI globally...")
            if sys.platform == "win32":
                print("On Windows, run: install_global.bat --uninstall")
            else:
                print("On Unix systems, run: sudo ./install_global.sh")
            return
        
        print("Installing FluxUI globally...")
        
        if sys.platform == "win32":
            print("On Windows, run: install_global.bat")
            print("(Right-click and 'Run as administrator')")
        else:
            print("On Unix systems, run: sudo ./install_global.sh")
        
        print("\nAfter installation:")
        print("- Commands available globally: fluxui, fluxui-cli, fluxui-ide")
        print("- .flux files will open with FluxUI IDE")
        print("- Desktop shortcuts created")
    
    def cmd_check_global(self):
        """Check global installation status"""
        print("🔍 Checking FluxUI Global Installation")
        print("=" * 45)
        
        # Check if commands are available
        commands = ["fluxui", "fluxui-cli", "fluxui-ide"]
        
        for cmd in commands:
            try:
                result = subprocess.run([cmd, "--version"], 
                                     capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ {cmd}: Available")
                    print(f"   {result.stdout.strip()}")
                else:
                    print(f"❌ {cmd}: Not working")
            except FileNotFoundError:
                print(f"❌ {cmd}: Not found")
            except subprocess.TimeoutExpired:
                print(f"⏰ {cmd}: Timeout")
            except Exception as e:
                print(f"❌ {cmd}: Error - {e}")
        
        # Check file associations
        if sys.platform == "win32":
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, ".flux")
                file_type = winreg.QueryValue(key, None)
                winreg.CloseKey(key)
                
                if file_type == "FluxUIFile":
                    print("✅ File associations: Working")
                else:
                    print("❌ File associations: Incorrect")
            except:
                print("❌ File associations: Not found")
        else:
            print("📁 File associations: Check with 'fluxui doctor'")
        
        # Check PATH
        if sys.platform == "win32":
            import winreg
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                 r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment")
                path_value = winreg.QueryValueEx(key, "PATH")[0]
                winreg.CloseKey(key)
                
                if "FluxUI" in path_value:
                    print("✅ PATH: FluxUI in system PATH")
                else:
                    print("❌ PATH: FluxUI not in system PATH")
            except:
                print("❓ PATH: Could not check system PATH")
        else:
            path_env = os.environ.get("PATH", "")
            if "/usr/local/bin" in path_env:
                print("✅ PATH: /usr/local/bin in PATH")
            else:
                print("❌ PATH: /usr/local/bin not in PATH")
    
    def create_project_structure(self, path, name, template):
        """Create project structure"""
        # Create directories
        dirs = ["src", "tests", "docs", "samples"]
        for dir_name in dirs:
            os.makedirs(os.path.join(path, dir_name), exist_ok=True)
        
        # Create main.flux
        main_content = self.get_template_content(template, name)
        with open(os.path.join(path, "main.flux"), "w") as f:
            f.write(main_content)
        
        # Create README.md
        readme_content = f"""# {name}

A FluxUI project created with the {template} template.

## Getting Started

```bash
fluxui run main.flux
```

## Project Structure

- `main.flux` - Main application file
- `src/` - Source files
- `tests/` - Test files
- `docs/` - Documentation
- `samples/` - Sample code

## Learn More

- [FluxUI Documentation](https://fluxui-lang.org)
- [Language Reference](docs/language-reference.md)
"""
        
        with open(os.path.join(path, "README.md"), "w") as f:
            f.write(readme_content)
        
        # Create project config
        project_config = {
            "name": name,
            "version": "1.0.0",
            "template": template,
            "author": self.config.get("author", "FluxUI Developer")
        }
        
        with open(os.path.join(path, "project.json"), "w") as f:
            json.dump(project_config, f, indent=2)
    
    def get_template_content(self, template, name):
        """Get template content"""
        templates = {
            "basic": f'''# Basic FluxUI Application
# Project: {name}

APP "{name}" 400 300

VAR message = "Hello, FluxUI!"

LABEL title {{
    TEXT: message
    FONT_SIZE: 16
    X: 20
    Y: 20
}}

BUTTON btn {{
    TEXT: "Click Me"
    X: 20
    Y: 60
    ONCLICK: {{
        PRINT "Button clicked!"
        SET message = "Button was clicked!"
        SET_TEXT title message
    }}
}}
''',
            "ui": f'''# UI Application
# Project: {name}

APP "{name}" 800 600

VAR counter = 0

FRAME main_frame {{
    WIDTH: 780
    HEIGHT: 580
    PADDING: 10
    
    LABEL title {{
        TEXT: "{name}"
        FONT_SIZE: 20
        X: 10
        Y: 10
    }}
    
    ROW controls {{
        Y: 50
        SPACING: 10
        
        BUTTON increment_btn {{
            TEXT: "Increment"
            ONCLICK: {{
                SET counter += 1
                SET_TEXT counter_label "Count: " + counter
            }}
        }}
        
        BUTTON decrement_btn {{
            TEXT: "Decrement"
            ONCLICK: {{
                SET counter -= 1
                SET_TEXT counter_label "Count: " + counter
            }}
        }}
        
        BUTTON reset_btn {{
            TEXT: "Reset"
            ONCLICK: {{
                SET counter = 0
                SET_TEXT counter_label "Count: 0"
            }}
        }}
    }}
    
    LABEL counter_label {{
        TEXT: "Count: 0"
        FONT_SIZE: 14
        X: 10
        Y: 100
    }}
}}
''',
            "data": f'''# Data Visualization Application
# Project: {name}

APP "{name}" 1000 700

VAR sample_data = [
    ["Jan", 100], ["Feb", 150], ["Mar", 120],
    ["Apr", 200], ["May", 180], ["Jun", 250]
]

FRAME main_frame {{
    WIDTH: 980
    HEIGHT: 680
    PADDING: 10
    
    LABEL title {{
        TEXT: "{name} - Data Visualization"
        FONT_SIZE: 20
        X: 10
        Y: 10
    }}
    
    LINE_PLOT sales_chart {{
        WIDTH: 450
        HEIGHT: 300
        TITLE: "Monthly Sales Trend"
        X_LABEL: "Month"
        Y_LABEL: "Sales ($)"
        X: 10
        Y: 50
        DATA: sample_data
    }}
    
    BAR_CHART sales_bar {{
        WIDTH: 450
        HEIGHT: 300
        TITLE: "Sales by Month"
        X: 500
        Y: 50
        CATEGORIES: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
        VALUES: [100, 150, 120, 200, 180, 250]
    }}
}}
''',
            "empty": f'''# Empty FluxUI Project
# Project: {name}

APP "{name}" 400 300

# Add your code here
PRINT "Hello, FluxUI!"
'''
        }
        
        return templates.get(template, templates["empty"])
    
    def create_project_files(self, path):
        """Create project files"""
        # Create .fluxignore
        with open(os.path.join(path, ".fluxignore"), "w") as f:
            f.write("""# FluxUI ignore file
__pycache__/
*.pyc
build/
dist/
.fluxui_build/
""")
        
        # Create .fluxui directory structure
        os.makedirs(".fluxui/cache", exist_ok=True)
        os.makedirs(".fluxui/logs", exist_ok=True)
    
    def open_ide(self, project_path):
        """Open project in IDE"""
        try:
            subprocess.Popen([sys.executable, "fluxui_ide.py", project_path])
        except:
            print("⚠️  Could not open IDE")
    
    def check_python(self):
        """Check Python installation"""
        return sys.version_info >= (3, 7)
    
    def check_dependencies(self):
        """Check dependencies"""
        try:
            import customtkinter
            return True
        except ImportError:
            return False
    
    def check_config(self):
        """Check configuration"""
        return os.path.exists(self.config_file)
    
    def check_installation(self):
        """Check FluxUI installation"""
        return os.path.exists("fluxui.py")
    
    def show_help(self):
        """Show comprehensive help"""
        help_text = """
╦ ╦╔═╗╔╗ ╔╦╗╔═╗╔╦╗╔═╗╦  ╔═╗╔╦╗╔═╗
║║║║╣ ╠╩╗ ║ ║╣ ║║║╠═╝║  ╠═╣ ║ ║╣ 
╚╩╝╚═╝╚═╝ ╩ ╚═╝╩ ╩╩  ╩═╝╩ ╩ ╩ ╚═╝
                                    
Modern UI Programming Language - Version {}

╔══════════════════════════════════════════════════════════════╗
║                        QUICK START                          ║
╚══════════════════════════════════════════════════════════════╝

Create your first project:
  fluxui new myapp
  cd myapp
  fluxui run main.flux

╔══════════════════════════════════════════════════════════════╗
║                    PROJECT COMMANDS                           ║
╚══════════════════════════════════════════════════════════════╝

  new <name>              Create a new FluxUI project
    -t, --template TYPE    Project template (basic|ui|data|empty)
    -p, --path PATH        Project directory
    --ide                  Open in IDE after creation

  run <file>               Run a FluxUI program
    --gui                  Run with GUI interface
    --debug                Enable debug mode

  test [path]              Run tests
    --watch                Watch mode for continuous testing

  build [path]             Build executable from project
    -o, --output FILE      Output file name
    --release              Release build optimization

  clean [path]             Clean build artifacts and temporary files

╔══════════════════════════════════════════════════════════════╗
║                   PACKAGE MANAGEMENT                          ║
╚══════════════════════════════════════════════════════════════╝

  install [package]        Install FluxUI packages
    --global               Install globally for all users

  uninstall <package>      Remove installed packages

  list                     List all installed packages
    --global               Show global packages only

  search <query>           Search for available packages

╔══════════════════════════════════════════════════════════════╗
║                    CONFIGURATION                              ║
╚══════════════════════════════════════════════════════════════╝

  config                   Manage FluxUI configuration
    --list                 Show all configuration
    --reset                Reset to defaults
    [KEY] [VALUE]          Get or set configuration values

  init                     Initialize FluxUI environment
    --force                Force initialization

  doctor                   Check system health and dependencies

╔══════════════════════════════════════════════════════════════╗
║                    UTILITIES                                ║
╚══════════════════════════════════════════════════════════════╝

  update                   Update FluxUI to latest version
    --check               Check for updates only

  docs [topic]             Open documentation
    api                   API documentation
    tutorials             Step-by-step guides
    reference             Language reference

  samples                  Manage sample projects
    --list                List available samples
    --create              Create sample project
    [NAME]                Specific sample details

  install-global          Install FluxUI globally
    --force               Force installation
    --uninstall           Uninstall global installation

  check-global            Check global installation status

╔══════════════════════════════════════════════════════════════╗
║                     EXAMPLES                                  ║
╚══════════════════════════════════════════════════════════════╝

  Create a basic UI app:
    fluxui new calculator --template=basic --ide

  Run with GUI:
    fluxui run app.flux --gui

  Build for distribution:
    fluxui build --release --output=myapp.exe

  Install globally:
    fluxui install-global

  Check global installation:
    fluxui check-global

  Check system:
    fluxui doctor

  View documentation:
    fluxui docs api

╔══════════════════════════════════════════════════════════════╗
║                    LEARNING RESOURCES                         ║
╚══════════════════════════════════════════════════════════════╝

  Website: https://fluxui-lang.org
  GitHub:  https://github.com/zerogravitygamingx211-hash/FluxUI
  Discord: https://discord.gg/fluxui
  Docs:    fluxui docs

╔══════════════════════════════════════════════════════════════╗
║                     TROUBLESHOOTING                            ║
╚══════════════════════════════════════════════════════════════╝

  Installation issues:    fluxui doctor
  Permission errors:     Run as administrator
  PATH issues:          fluxui config --list
  File associations:    fluxui init --force

For detailed help on any command:
  fluxui <command> --help

Happy coding with FluxUI! ⚡
""".format(self.version)
        
        print(help_text)
    
    def run(self):
        """Run the CLI"""
        parser = self.create_parser()
        args = parser.parse_args()
        
        if args.verbose:
            print(f"🔧 FluxUI CLI v{self.version}")
        
        self.handle_command(args)


if __name__ == "__main__":
    cli = FluxUICLI()
    cli.run()
