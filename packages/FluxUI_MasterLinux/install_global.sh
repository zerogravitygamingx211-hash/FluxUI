#!/bin/bash

# FluxUI Global Installer for Linux/macOS
# Usage: sudo ./install_global.sh

echo "FluxUI Global Installer"
echo "======================="
echo

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "ERROR: Root privileges required"
    echo "Please run: sudo ./install_global.sh"
    exit 1
fi

# Detect system
if [ "$(uname)" = "Darwin" ]; then
    SYSTEM="macos"
    INSTALL_DIR="/usr/local"
else
    SYSTEM="linux"
    INSTALL_DIR="/usr/local"
fi

echo "System: $SYSTEM"
echo "Install directory: $INSTALL_DIR"
echo

# Create directories
echo "Creating directories..."
mkdir -p "$INSTALL_DIR/bin"
mkdir -p "$INSTALL_DIR/lib/fluxui"
mkdir -p "$INSTALL_DIR/lib/fluxui/core"
mkdir -p "$INSTALL_DIR/share/fluxui"
mkdir -p "$INSTALL_DIR/share/doc/fluxui"
mkdir -p "$INSTALL_DIR/share/applications"
mkdir -p "/etc/fluxui"

# Copy library files
echo "Installing libraries..."
cp fluxui.py "$INSTALL_DIR/lib/fluxui/core/" 2>/dev/null || echo "Warning: fluxui.py not found"
cp fluxui_cli.py "$INSTALL_DIR/lib/fluxui/core/" 2>/dev/null || echo "Warning: fluxui_cli.py not found"
cp fluxui_ide.py "$INSTALL_DIR/lib/fluxui/core/" 2>/dev/null || echo "Warning: fluxui_ide.py not found"
cp parser.py "$INSTALL_DIR/lib/fluxui/core/" 2>/dev/null || echo "Warning: parser.py not found"
cp tokenizer.py "$INSTALL_DIR/lib/fluxui/core/" 2>/dev/null || echo "Warning: tokenizer.py not found"
cp parser_ast.py "$INSTALL_DIR/lib/fluxui/core/" 2>/dev/null || echo "Warning: parser_ast.py not found"
cp engine.py "$INSTALL_DIR/lib/fluxui/core/" 2>/dev/null || echo "Warning: engine.py not found"
cp ui_engine.py "$INSTALL_DIR/lib/fluxui/core/" 2>/dev/null || echo "Warning: ui_engine.py not found"
cp components.py "$INSTALL_DIR/lib/fluxui/core/" 2>/dev/null || echo "Warning: components.py not found"
cp renderer.py "$INSTALL_DIR/lib/fluxui/core/" 2>/dev/null || echo "Warning: renderer.py not found"
cp flux_runner.py "$INSTALL_DIR/lib/fluxui/core/" 2>/dev/null || echo "Warning: flux_runner.py not found"

# Copy documentation
echo "Installing documentation..."
cp FluxUI_Language_Reference.md "$INSTALL_DIR/share/doc/fluxui/" 2>/dev/null || echo "Warning: FluxUI_Language_Reference.md not found"
cp README.md "$INSTALL_DIR/share/doc/fluxui/" 2>/dev/null || echo "Warning: README.md not found"
cp fluxui.svg "$INSTALL_DIR/share/fluxui/" 2>/dev/null || echo "Warning: fluxui.svg not found"

# Create executable scripts
echo "Creating executables..."

# fluxui
cat > "$INSTALL_DIR/bin/fluxui" << 'EOF'
#!/bin/bash
python "$INSTALL_DIR/lib/fluxui/core/fluxui.py" "$@"
EOF

# fluxui-cli
cat > "$INSTALL_DIR/bin/fluxui-cli" << 'EOF'
#!/bin/bash
python "$INSTALL_DIR/lib/fluxui/core/fluxui_cli.py" "$@"
EOF

# fluxui-ide
cat > "$INSTALL_DIR/bin/fluxui-ide" << 'EOF'
#!/bin/bash
python "$INSTALL_DIR/lib/fluxui/core/fluxui_ide.py" "$@"
EOF

# Make executables executable
chmod +x "$INSTALL_DIR/bin/fluxui"
chmod +x "$INSTALL_DIR/bin/fluxui-cli"
chmod +x "$INSTALL_DIR/bin/fluxui-ide"

# Set up file associations
echo "Setting up file associations..."

# Create MIME type
cat > /usr/share/mime/packages/fluxui.xml << 'EOF'
<?xml version="1.0"?>
<mime-info xmlns='http://www.freedesktop.org/standards/shared-mime-info'>
  <mime-type type="text/x-fluxui">
    <comment>FluxUI Source File</comment>
    <glob pattern="*.flux"/>
  </mime-type>
</mime-info>
EOF

# Update MIME database
if command -v update-mime-database &> /dev/null; then
    update-mime-database /usr/share/mime
fi

# Create desktop entry
cat > "$INSTALL_DIR/share/applications/fluxui-ide.desktop" << 'EOF'
[Desktop Entry]
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
EOF

# Update desktop database
if command -v update-desktop-database &> /dev/null; then
    update-desktop-database "$INSTALL_DIR/share/applications"
fi

# Create user config directory (for non-root user)
USER_HOME=$(getent passwd 1000 | cut -d: -f6)
if [ -n "$USER_HOME" ]; then
    USER_CONFIG="$USER_HOME/.config/fluxui"
    mkdir -p "$USER_CONFIG"
    
    cat > "$USER_CONFIG/config.json" << EOF
{
  "version": "Beta 1.0",
  "install_path": "$INSTALL_DIR/lib/fluxui",
  "global_install": true,
  "system": "$SYSTEM"
}
EOF
    
    chown -R 1000:1000 "$USER_CONFIG" 2>/dev/null || true
fi

# Create system-wide config
cat > "/etc/fluxui/config.json" << EOF
{
  "version": "Beta 1.0",
  "install_path": "$INSTALL_DIR/lib/fluxui",
  "global_install": true,
  "system": "$SYSTEM"
}
EOF

echo
echo "========================================"
echo "Global Installation Complete!"
echo "========================================"
echo
echo "Installation directory: $INSTALL_DIR"
echo
echo "Commands now available globally:"
echo "  fluxui        - Run FluxUI programs"
echo "  fluxui-cli    - Modern CLI interface"
echo "  fluxui-ide    - Integrated Development Environment"
echo
echo "File associations:"
echo "  .flux files now open with FluxUI IDE"
echo
echo "Desktop entry created:"
echo "  Applications > Programming > FluxUI IDE"
echo
echo "Testing installation..."
echo

# Test installation
sleep 2
if command -v fluxui &> /dev/null; then
    echo "SUCCESS: fluxui command found!"
    fluxui --version 2>/dev/null || echo "Note: fluxui --version test failed (may need PATH refresh)"
else
    echo "ERROR: fluxui command not found"
    echo "You may need to restart your terminal or run:"
    echo "  source ~/.bashrc"
fi

echo
echo "Installation complete!"
echo
echo "Note: You may need to restart your terminal"
echo "or run 'source ~/.bashrc' for PATH changes."
echo
