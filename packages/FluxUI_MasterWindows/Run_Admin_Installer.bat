@echo off
title FluxUI Setup - Administrator Required

echo ========================================
echo   FluxUI Programming Language
echo   Administrator Setup Required
echo ========================================
echo.
echo This installer requires administrator privileges to:
echo - Install files to Program Files
echo - Add FluxUI to system PATH
echo - Create file associations
echo - Create desktop shortcuts
echo.
echo Please run this file as administrator:
echo 1. Right-click this file
echo 2. Select "Run as administrator"
echo 3. Click "Yes" when prompted
echo.
echo Press any key to continue...
pause > nul

echo Starting FluxUI Setup Wizard...
python fluxui_wizard_compact.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Setup failed
    echo Make sure Python is installed and run as administrator
    pause
    exit /b 1
)

echo.
echo ========================================
echo   FluxUI Setup Complete!
echo ========================================
echo.
echo You can now run: fluxui --ver
echo.
echo This window will close in 5 seconds...
timeout /t 5 /nobreak >nul
