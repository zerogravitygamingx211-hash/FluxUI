@echo off
echo Installing FluxUI file association...
echo.

REM Create file association for .flux extension
assoc .flux=FluxUIFile
if %errorlevel% neq 0 (
    echo Error: Failed to create file association
    pause
    exit /b 1
)

REM Set the command to execute .flux files
ftype FluxUIFile="fluxui.exe" "%%1"
if %errorlevel% neq 0 (
    echo Error: Failed to set executable command
    pause
    exit /b 1
)

REM Add to PATH if not already present
echo Adding FluxUI to system PATH...

REM Get current directory
set "FLUX_DIR=%~dp0"
set "FLUX_DIR=%FLUX_DIR:~0,-1%"

REM Check if already in PATH
echo %PATH% | findstr /i /c:"%FLUX_DIR%" >nul
if %errorlevel% neq 0 (
    echo Adding %FLUX_DIR% to PATH...
    setx PATH "%PATH%;%FLUX_DIR%" /M
    if %errorlevel% neq 0 (
        echo Warning: Could not add to system PATH (run as administrator)
        echo You may need to add %FLUX_DIR% to PATH manually
    )
) else (
    echo FluxUI directory already in PATH
)

echo.
echo Installation complete!
echo You can now run: fluxui filename.flux
echo Or double-click .flux files to execute them
echo.
pause
