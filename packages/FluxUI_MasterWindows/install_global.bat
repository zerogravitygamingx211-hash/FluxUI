@echo off
echo FluxUI Global Installer
echo =====================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Administrator privileges required
    echo Please right-click this file and select "Run as administrator"
    pause
    exit /b 1
)

echo Installing FluxUI globally...
echo.

REM Set installation directory
set "INSTALL_DIR=%ProgramFiles%\FluxUI"

REM Create directories
echo Creating directories...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
if not exist "%INSTALL_DIR%\bin" mkdir "%INSTALL_DIR%\bin"
if not exist "%INSTALL_DIR%\lib" mkdir "%INSTALL_DIR%\lib"
if not exist "%INSTALL_DIR%\lib\core" mkdir "%INSTALL_DIR%\lib\core"
if not exist "%INSTALL_DIR%\docs" mkdir "%INSTALL_DIR%\docs"
if not exist "%INSTALL_DIR%\share" mkdir "%INSTALL_DIR%\share"

REM Copy library files
echo Installing libraries...
copy "fluxui.py" "%INSTALL_DIR%\lib\core\" >nul
copy "fluxui_cli.py" "%INSTALL_DIR%\lib\core\" >nul
copy "fluxui_ide.py" "%INSTALL_DIR%\lib\core\" >nul
copy "parser.py" "%INSTALL_DIR%\lib\core\" >nul
copy "tokenizer.py" "%INSTALL_DIR%\lib\core\" >nul
copy "parser_ast.py" "%INSTALL_DIR%\lib\core\" >nul
copy "engine.py" "%INSTALL_DIR%\lib\core\" >nul
copy "ui_engine.py" "%INSTALL_DIR%\lib\core\" >nul
copy "components.py" "%INSTALL_DIR%\lib\core\" >nul
copy "renderer.py" "%INSTALL_DIR%\lib\core\" >nul
copy "flux_runner.py" "%INSTALL_DIR%\lib\core\" >nul

REM Copy documentation
echo Installing documentation...
copy "FluxUI_Language_Reference.md" "%INSTALL_DIR%\docs\" >nul
copy "README.md" "%INSTALL_DIR%\docs\" >nul
copy "fluxui.svg" "%INSTALL_DIR%\share\" >nul

REM Create executable scripts
echo Creating executables...

REM fluxui.exe
(
echo @echo off
echo python "%INSTALL_DIR%\lib\core\fluxui.py" %%*
) > "%INSTALL_DIR%\bin\fluxui.bat"

REM fluxui-cli.exe
(
echo @echo off
echo python "%INSTALL_DIR%\lib\core\fluxui_cli.py" %%*
) > "%INSTALL_DIR%\bin\fluxui-cli.bat"

REM fluxui-ide.exe
(
echo @echo off
echo python "%INSTALL_DIR%\lib\core\fluxui_ide.py" %%*
) > "%INSTALL_DIR%\bin\fluxui-ide.bat"

REM Create Windows executables (batch files renamed to .exe)
copy "%INSTALL_DIR%\bin\fluxui.bat" "%INSTALL_DIR%\bin\fluxui.exe" >nul
copy "%INSTALL_DIR%\bin\fluxui-cli.bat" "%INSTALL_DIR%\bin\fluxui-cli.exe" >nul
copy "%INSTALL_DIR%\bin\fluxui-ide.bat" "%INSTALL_DIR%\bin\fluxui-ide.exe" >nul

REM Add to system PATH
echo Adding to system PATH...
setx PATH "%PATH%;%INSTALL_DIR%\bin" /M >nul

REM Set up file associations
echo Setting up file associations...
assoc .flux=FluxUIFile >nul
ftype FluxUIFile="%INSTALL_DIR%\bin\fluxui-ide.exe" "%%1" >nul

REM Create desktop shortcut
echo Creating desktop shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%PUBLIC%\Desktop\FluxUI IDE.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\bin\fluxui-ide.exe'; $Shortcut.Save()" >nul

REM Create Start Menu shortcut
echo Creating Start Menu shortcut...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%ProgramData%\Microsoft\Windows\Start Menu\Programs\FluxUI IDE.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\bin\fluxui-ide.exe'; $Shortcut.Save()" >nul

REM Create configuration
echo Creating configuration...
set "CONFIG_DIR=%APPDATA%\FluxUI"
if not exist "%CONFIG_DIR%" mkdir "%CONFIG_DIR%"
(
echo {
echo   "version": "Beta 1.0",
echo   "install_path": "%INSTALL_DIR%",
echo   "global_install": true,
echo   "system": "windows"
echo }
) > "%CONFIG_DIR%\config.json"

echo.
echo ========================================
echo Global Installation Complete!
echo ========================================
echo.
echo Installation directory: %INSTALL_DIR%
echo.
echo Commands now available globally:
echo   fluxui        - Run FluxUI programs
echo   fluxui-cli    - Modern CLI interface  
echo   fluxui-ide    - Integrated Development Environment
echo.
echo File associations:
echo   .flux files now open with FluxUI IDE
echo.
echo Shortcuts created:
echo   Desktop: FluxUI IDE
echo   Start Menu: FluxUI IDE
echo.
echo You may need to restart your terminal or system
echo for PATH changes to take effect.
echo.
echo Testing installation...
echo.

REM Test installation
timeout /t 2 >nul
fluxui --version
if %errorlevel% equ 0 (
    echo SUCCESS: fluxui command working!
) else (
    echo ERROR: fluxui command not working yet
    echo You may need to restart your terminal
)

echo.
echo Installation complete! Press any key to exit...
pause >nul
