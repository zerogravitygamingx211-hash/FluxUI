@echo off
title FluxUI Installer
color 0A

echo ========================================
echo   FluxUI Programming Language
echo   Simple Installer
echo ========================================
echo.
echo This will install FluxUI to:
echo C:\Program Files\FluxUI
echo.
echo Press any key to continue...
pause > nul

echo.
echo Creating installation directory...
if not exist "C:\Program Files\FluxUI" (
    mkdir "C:\Program Files\FluxUI"
    mkdir "C:\Program Files\FluxUI\bin"
    mkdir "C:\Program Files\FluxUI\lib"
    mkdir "C:\Program Files\FluxUI\docs"
    mkdir "C:\Program Files\FluxUI\samples"
)

echo Copying files...
copy "FluxUI.exe" "C:\Program Files\FluxUI\bin\" > nul
copy "fluxui-cli.exe" "C:\Program Files\FluxUI\bin\" > nul
copy "fluxui.py" "C:\Program Files\FluxUI\lib\" > nul
copy "parser.py" "C:\Program Files\FluxUI\lib\" > nul
copy "tokenizer.py" "C:\Program Files\FluxUI\lib\" > nul
copy "engine.py" "C:\Program Files\FluxUI\lib\" > nul
copy "components.py" "C:\Program Files\FluxUI\lib\" > nul
copy "ui_engine.py" "C:\Program Files\FluxUI\lib\" > nul
copy "fluxui_cli.py" "C:\Program Files\FluxUI\lib\" > nul
copy "fluxui_ide.py" "C:\Program Files\FluxUI\lib\" > nul
copy "FluxUI_Language_Reference.md" "C:\Program Files\FluxUI\docs\" > nul
copy "FluxUI_Instruction_Book.md" "C:\Program Files\FluxUI\docs\" > nul
copy "Test.flux" "C:\Program Files\FluxUI\samples\" > nul
copy "test_executable.flux" "C:\Program Files\FluxUI\samples\" > nul

echo Creating fluxui.exe alias...
copy "C:\Program Files\FluxUI\bin\FluxUI.exe" "C:\Program Files\FluxUI\bin\fluxui.exe" > nul

echo Adding to system PATH...
setx PATH "%PATH%;C:\Program Files\FluxUI\bin" > nul

echo Creating file associations...
reg add "HKEY_CLASSES_ROOT\.flux" /ve /d "FluxUIFile" /f > nul
reg add "HKEY_CLASSES_ROOT\FluxUIFile" /ve /d "FluxUI Source File" /f > nul
reg add "HKEY_CLASSES_ROOT\FluxUIFile\DefaultIcon" /ve /d "C:\Program Files\FluxUI\bin\FluxUI.exe,0" /f > nul
reg add "HKEY_CLASSES_ROOT\FluxUIFile\shell\open\command" /ve /d "\"C:\Program Files\FluxUI\bin\FluxUI.exe\" \"%1\"" /f > nul

echo Creating desktop shortcut...
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%PUBLIC%\Desktop\FluxUI.lnk'); $Shortcut.TargetPath = 'C:\Program Files\FluxUI\bin\fluxui.exe'; $Shortcut.Description = 'FluxUI Programming Language'; $Shortcut.Save()"

echo.
echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo FluxUI has been installed to:
echo C:\Program Files\FluxUI
echo.
echo You can now run:
echo fluxui --ver
echo fluxui program.flux
echo.
echo Please restart Command Prompt to use fluxui command.
echo.
pause
