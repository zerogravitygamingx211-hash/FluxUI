@echo off
echo Installing FluxIDE executable...

REM Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Please run this script as Administrator to install to system directory
    echo Installing to user directory instead...
    set "DEST_DIR=%USERPROFILE%\bin"
) else (
    set "DEST_DIR=C:\Windows\System32"
)

REM Create destination directory if it doesn't exist
if not exist "%DEST_DIR%" (
    mkdir "%DEST_DIR%"
)

REM Copy executable
copy "dist_executables\FluxIDE.exe" "%DEST_DIR%\" /Y
if %errorlevel% neq 0 (
    echo Error: Failed to copy executable
    pause
    exit /b 1
)

echo FluxIDE installed successfully!
echo You can now run 'FluxIDE' from anywhere
echo.
pause
