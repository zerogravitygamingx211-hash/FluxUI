#!/usr/bin/env python3
"""
Simple FluxUI Icon Creator
Creates basic icons without encoding issues
"""
import os

def create_simple_ascii_icon():
    """Create simple ASCII icon"""
    ascii_icon = """
     _______  _______  _______  _______ 
    |       ||       ||       ||       |
    | FLUXUI||  IDE  ||  CLI  ||  LANG |
    |_______||_______||_______||_______|
    
    Modern UI Programming Language
    Version Beta 1.0
    
     .--.                   .--.
    |o_o |                  | !_ |
    |:_/ |                  | _ |  
    //   \\  .--.           //   \\ 
   (|     | |o_o |          (|     |) 
    \\_   // |:_/ |          \\_   // 
     |_| `'  //   \\            |_| `'
           (|     |)               
            \\_   //             
             |_| '              
    """
    
    with open("fluxui_ascii.txt", "w") as f:
        f.write(ascii_icon)
    
    print("ASCII icon created: fluxui_ascii.txt")

def create_simple_svg():
    """Create simple SVG icon"""
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
    <!-- Background rounded rectangle -->
    <rect x="32" y="32" width="192" height="192" rx="24" fill="#2980b9"/>
    
    <!-- Lightning bolt symbol -->
    <path d="M 102 51 L 89 128 L 154 128 L 128 205 L 166 128 L 102 128 L 128 51 Z" 
          fill="white" stroke="none"/>
    
    <!-- F text -->
    <text x="128" y="220" font-family="Arial, sans-serif" font-size="24" 
          font-weight="bold" text-anchor="middle" fill="white">F</text>
</svg>'''
    
    with open("fluxui.svg", "w") as f:
        f.write(svg_content)
    
    print("SVG icon created: fluxui.svg")

def create_desktop_entry():
    """Create Linux desktop entry"""
    desktop_entry = '''[Desktop Entry]
Version=1.0
Type=Application
Name=FluxUI IDE
Comment=FluxUI Integrated Development Environment
Exec=fluxui-ide
Icon=fluxui
Terminal=false
Categories=Development;IDE;
Keywords=programming;language;ui;development;
StartupWMClass=FluxUI_IDE
'''
    
    with open("fluxui-ide.desktop", "w") as f:
        f.write(desktop_entry)
    
    print("Desktop entry created: fluxui-ide.desktop")

def create_icon_manifest():
    """Create icon manifest"""
    manifest = '''{
  "name": "FluxUI",
  "version": "Beta 1.0",
  "description": "Modern UI Programming Language",
  "icons": {
    "svg": "fluxui.svg",
    "desktop": "fluxui-ide.desktop",
    "ascii": "fluxui_ascii.txt"
  },
  "theme": {
    "primary": "#2980b9",
    "secondary": "#3498db",
    "accent": "#ffffff"
  },
  "file_associations": {
    ".flux": "FluxUI Source File",
    "icon": "fluxui.svg"
  }
}'''
    
    with open("fluxui_icons.json", "w") as f:
        f.write(manifest)
    
    print("Icon manifest created: fluxui_icons.json")

def create_ico_placeholder():
    """Create a simple ICO placeholder description"""
    ico_info = '''FluxUI Icon Information
========================

For Windows users, the following icon sizes are recommended:
- 16x16 - Taskbar and small icons
- 32x32 - Desktop and file explorer
- 48x48 - Control panel
- 64x64 - High DPI displays
- 128x128 - Large icons
- 256x256 - Extra large icons

The icon features:
- Blue rounded rectangle background (#2980b9)
- White lightning bolt symbol
- "F" letter for FluxUI
- Modern, clean design

To create proper ICO files:
1. Use an image editor (GIMP, Photoshop)
2. Create the design at 256x256
3. Export as ICO with multiple sizes
4. Save as fluxui.ico

Or use online converters:
- Convert fluxui.svg to ICO
- Use icon generator websites
'''
    
    with open("fluxui_icon_info.txt", "w") as f:
        f.write(ico_info)
    
    print("Icon info created: fluxui_icon_info.txt")

if __name__ == "__main__":
    print("Creating FluxUI Icons...")
    print("=" * 40)
    
    create_simple_ascii_icon()
    create_simple_svg()
    create_desktop_entry()
    create_icon_manifest()
    create_ico_placeholder()
    
    print("\nBasic icon files created!")
    print("\nGenerated files:")
    print("- fluxui.svg (SVG icon for web)")
    print("- fluxui_ascii.txt (ASCII art for terminal)")
    print("- fluxui-ide.desktop (Linux desktop entry)")
    print("- fluxui_icons.json (Icon manifest)")
    print("- fluxui_icon_info.txt (Windows ICO info)")
    
    print("\nFor IDE integration:")
    print("- Use fluxui.svg for modern IDEs")
    print("- Convert to .ico for Windows")
    print("- Use fluxui-ide.desktop for Linux")
    print("- ASCII art works in terminals")
