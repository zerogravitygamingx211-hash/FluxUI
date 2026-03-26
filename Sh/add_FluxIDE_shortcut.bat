@echo off
echo Creating FluxIDE desktop shortcut...

set "SHORTCUT=%USERPROFILE%\Desktop\FluxIDE.lnk"
set "TARGET=%CD%\dist_executables\FluxIDE.exe"

powershell -command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%SHORTCUT%'); $s.TargetPath = '%TARGET%'; $s.Save()"

echo Desktop shortcut created: %SHORTCUT%
pause
