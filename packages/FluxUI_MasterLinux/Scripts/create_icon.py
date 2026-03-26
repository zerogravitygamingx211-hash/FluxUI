#!/usr/bin/env python3
"""
Create FluxUI Icons
Generates icons for the FluxUI programming language
"""
import os
from PIL import Image, ImageDraw, ImageFont
import json

def create_fluxui_icon():
    """Create FluxUI icon with lightning bolt theme"""
    
    # Create multiple sizes for different uses
    sizes = [16, 32, 48, 64, 128, 256]
    
    for size in sizes:
        # Create image with transparent background
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Colors - modern blue theme
        bg_color = (41, 128, 185)  # Blue background
        bolt_color = (255, 255, 255)  # White lightning bolt
        accent_color = (52, 152, 219)  # Light blue accent
        
        # Draw rounded rectangle background
        margin = size // 8
        draw.rounded_rectangle(
            [margin, margin, size - margin, size - margin],
            radius=size // 8,
            fill=bg_color
        )
        
        # Draw lightning bolt
        if size >= 32:
            # Lightning bolt coordinates (scaled)
            bolt_points = [
                (size * 0.4, size * 0.2),   # Top left
                (size * 0.35, size * 0.5),  # Middle left
                (size * 0.6, size * 0.5),   # Middle right
                (size * 0.5, size * 0.8),    # Bottom right
                (size * 0.65, size * 0.8),   # Bottom right (extended)
                (size * 0.45, size * 0.4),   # Middle
                (size * 0.7, size * 0.4),   # Middle right (top)
                (size * 0.6, size * 0.2),    # Top right
            ]
            
            # Simplify for smaller sizes
            if size < 64:
                bolt_points = [
                    (size * 0.4, size * 0.2),
                    (size * 0.3, size * 0.5),
                    (size * 0.7, size * 0.5),
                    (size * 0.5, size * 0.8),
                    (size * 0.6, size * 0.8),
                    (size * 0.4, size * 0.4),
                    (size * 0.6, size * 0.4),
                    (size * 0.5, size * 0.2),
                ]
            
            draw.polygon(bolt_points, fill=bolt_color)
        
        # Add "F" for FluxUI in larger icons
        if size >= 48:
            try:
                font_size = size // 4
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            text = "F"
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            text_x = (size - text_width) // 2
            text_y = size - text_height - margin - 2
            
            draw.text((text_x, text_y), text, fill=bolt_color, font=font)
        
        # Save the icon
        img.save(f"fluxui_icon_{size}x{size}.png")
        
        # Also save as ICO for Windows
        if size == 256:
            img.save("fluxui.ico", format="ICO", sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
    
    print("FluxUI icons created successfully!")

def create_ascii_icon():
    """Create ASCII art icon for terminal use"""
    ascii_icon = """
    ⚡ FLUXUI ⚡
    
     ╦ ╦╔═╗╔╗ ╔╦╗╔═╗╔╦╗╔═╗╦  ╔═╗╔╦╗╔═╗
     ║║║║╣ ╠╩╗ ║ ║╣ ║║║╠═╝║  ╠═╣ ║ ║╣ 
     ╚╩╝╚═╝╚═╝ ╩ ╚═╝╩ ╩╩  ╩═╝╩ ╩ ╩ ╚═╝
     
    Modern UI Programming Language
    """
    
    with open("fluxui_ascii.txt", "w") as f:
        f.write(ascii_icon)
    
    print("ASCII icon created: fluxui_ascii.txt")

def create_svg_icon():
    """Create SVG icon for web use"""
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg width="256" height="256" viewBox="0 0 256 256" xmlns="http://www.w3.org/2000/svg">
    <!-- Background -->
    <rect x="32" y="32" width="192" height="192" rx="24" fill="#2980b9"/>
    
    <!-- Lightning Bolt -->
    <path d="M 102 51 L 89 128 L 154 128 L 128 205 L 166 128 L 102 128 L 128 51 Z" 
          fill="white" stroke="none"/>
    
    <!-- F for FluxUI -->
    <text x="128" y="220" font-family="Arial, sans-serif" font-size="24" 
          font-weight="bold" text-anchor="middle" fill="white">F</text>
</svg>'''
    
    with open("fluxui.svg", "w") as f:
        f.write(svg_content)
    
    print("SVG icon created: fluxui.svg")

def create_desktop_entry():
    """Create Linux desktop entry file"""
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

def create_icon_resources():
    """Create icon resource file for Windows"""
    resource_content = '''
#ifndef FLUXUI_ICONS_H
#define FLUXUI_ICONS_H

// FluxUI Icon Resources
#define IDI_FLUXUI_ICON 101

#endif // FLUXUI_ICONS_H
'''
    
    with open("fluxui_icons.h", "w") as f:
        f.write(resource_content)
    
    print("Icon resource header created: fluxui_icons.h")

def create_icon_manifest():
    """Create icon manifest for IDE integration"""
    manifest = {
        "name": "FluxUI",
        "version": "Beta 1.0",
        "icons": {
            "16x16": "fluxui_icon_16x16.png",
            "32x32": "fluxui_icon_32x32.png", 
            "48x48": "fluxui_icon_48x48.png",
            "64x64": "fluxui_icon_64x64.png",
            "128x128": "fluxui_icon_128x128.png",
            "256x256": "fluxui_icon_256x256.png"
        },
        "formats": {
            "png": ["16x16", "32x32", "48x48", "64x64", "128x128", "256x256"],
            "ico": "fluxui.ico",
            "svg": "fluxui.svg"
        },
        "theme": {
            "primary": "#2980b9",
            "secondary": "#3498db", 
            "accent": "#ffffff",
            "style": "modern minimalist"
        },
        "usage": {
            "ide": "fluxui-ide",
            "cli": "fluxui",
            "file_association": ".flux",
            "installer": "fluxui_installer"
        }
    }
    
    with open("fluxui_icons.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    print("Icon manifest created: fluxui_icons.json")

if __name__ == "__main__":
    print("Creating FluxUI Icons...")
    print("=" * 40)
    
    try:
        create_fluxui_icon()
        create_ascii_icon()
        create_svg_icon()
        create_desktop_entry()
        create_icon_resources()
        create_icon_manifest()
        
        print("\nIcon creation complete!")
        print("\nGenerated files:")
        print("- fluxui.ico (Windows icon)")
        print("- fluxui.svg (SVG icon)")
        print("- fluxui_icon_*.png (PNG icons)")
        print("- fluxui_ascii.txt (ASCII art)")
        print("- fluxui-ide.desktop (Linux desktop entry)")
        print("- fluxui_icons.h (Windows resource header)")
        print("- fluxui_icons.json (Icon manifest)")
        
    except ImportError:
        print("PIL (Pillow) not installed. Creating basic icons only...")
        create_ascii_icon()
        create_svg_icon()
        create_desktop_entry()
        create_icon_resources()
        create_icon_manifest()
        
        print("\nBasic icons created!")
        print("Install PIL for full icon generation: pip install Pillow")
        
    except Exception as e:
        print(f"Error creating icons: {e}")
