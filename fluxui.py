#!/usr/bin/env python3
"""
FluxUI Main Executable
Usage: fluxui <filename.flux>
Compiles and executes FLUX language files
"""
import sys
import os
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
        description="FluxUI - Execute FLUX language files",
        prog="fluxui",
        epilog="Example: fluxui program.flux"
    )
    
    parser.add_argument(
        "file", 
        nargs='?',  # Make file argument optional
        help="FLUX source file to execute",
        metavar="FILE.flux"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="FluxUI Beta 1.0"
    )
    
    parser.add_argument(
        "--ver",
        action="version",
        version="FluxUI Beta 1.0"
    )
    
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Run with GUI interface (default: headless mode)"
    )
    
    args = parser.parse_args()
    
    # If no file provided and not asking for version, show help
    if not args.file and not (args.version or args.ver):
        parser.print_help()
        sys.exit(0)
    
    # Validate file extension if file is provided
    if args.file and not args.file.lower().endswith('.flux'):
        print(f"Error: File must have .flux extension")
        sys.exit(1)
    
    # Check if file exists
    if not os.path.exists(args.file):
        print(f"Error: File not found: {args.file}")
        sys.exit(1)
    
    try:
        if args.gui:
            # Run with GUI
            from ui_engine import FLUX
            from parser import FLUXParser
            
            engine = FLUX()
            parser_instance = FLUXParser(engine)
            success = parser_instance.compile(args.file)
            
            if parser_instance.errors:
                print("\n[COMPILE ERRORS]")
                for error in parser_instance.errors:
                    print(f"  {error}")
                sys.exit(1)
            
            # Start the GUI event loop
            engine.root.mainloop()
            
        else:
            # Run headless
            from flux_runner import run
            success = run(args.file)
            
            if not success:
                sys.exit(1)
                
        print(f"\n[SUCCESS] Executed {args.file}")
        
    except ImportError as e:
        print(f"Error: Missing dependency - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
