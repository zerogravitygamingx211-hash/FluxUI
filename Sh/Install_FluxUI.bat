@echo off
title FluxUI Auto Installer

echo ========================================
echo   FluxUI Programming Language
echo   Auto Installer
echo ========================================
echo.
echo This will automatically install FluxUI with:
echo - FluxUI.exe executable
echo - Global command-line tools
echo - .flux file associations
echo - System PATH configuration
echo - Desktop shortcuts
echo - FluxUI IDE
echo.
echo Starting installation...
echo.

python fluxui_auto_installer.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Installation failed
    echo Make sure Python is installed
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo FluxUI has been installed successfully!
echo.
echo You can now:
echo - Double-click .flux files to execute them
echo - Run 'fluxui --version' from command line
echo - Launch FluxUI IDE from desktop shortcut
echo.
echo Repository: https://github.com/zerogravitygamingx211-hash/FluxUI
echo.
echo This window will close in 5 seconds...
timeout /t 5 /nobreak >nul
