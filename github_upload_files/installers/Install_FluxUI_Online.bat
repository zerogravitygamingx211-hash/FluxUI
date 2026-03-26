@echo off
title FluxUI Online Installer

echo ========================================
echo   FluxUI Programming Language
echo   Online Installer
echo ========================================
echo.
echo This installer will download FluxUI components
echo from GitHub during installation.
echo.
echo Benefits:
echo - Smaller initial download size
echo - Always gets the latest version
echo - Automatic updates from repository
echo.
echo Repository: https://github.com/zerogravitygamingx211-hash/FluxUI
echo.
echo Starting online installer...
echo.

python fluxui_online_installer.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Installation failed
    echo Make sure Python is installed and you have internet connection
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Online Installation Complete!
echo ========================================
echo.
echo FluxUI has been installed from GitHub!
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
