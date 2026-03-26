@echo off
title FluxUI Executable Builder
echo.
echo ========================================
echo   FluxUI Executable Builder
echo ========================================
echo.
echo This will build all FluxUI executables:
echo - FluxUI.exe (main interpreter)
echo - fluxui-cli.exe (modern CLI)
echo - fluxui-ide.exe (IDE)
echo - FluxUI_Installer.exe (auto installer)
echo - FluxUI_Setup.exe (interactive wizard)
echo.
echo Starting build process...
echo.

python build_all_executables.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Build failed
    echo Check the error messages above
    pause
    exit /b 1
)

echo.
echo ========================================
echo   Build Complete!
echo ========================================
echo.
echo Executables created in: dist_executables\
echo Release package created in: FluxUI_Release\
echo.
echo Files ready for GitHub upload:
echo - Individual .exe files in dist_executables\
echo - Complete package in FluxUI_Release\
echo.
echo You can now upload these to your GitHub repository!
echo.
pause
