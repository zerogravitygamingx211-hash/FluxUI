@echo off
title FluxUI Setup Wizard
echo.
echo ========================================
echo   FluxUI Programming Language Setup
echo ========================================
echo.
echo This wizard will install FluxUI and configure:
echo - FluxUI.exe executable
echo - System PATH configuration
echo - .flux file associations
echo - FluxUI IDE
echo - Desktop shortcuts
echo.
echo Starting setup wizard...
echo.

python fluxui_wizard.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to start setup wizard
    echo Make sure Python is installed and fluxui_wizard.py exists
    pause
    exit /b 1
)

echo.
echo Setup wizard completed!
echo.
pause
