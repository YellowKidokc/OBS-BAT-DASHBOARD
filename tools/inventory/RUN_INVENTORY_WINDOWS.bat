@echo off
setlocal
REM Phase One READ-ONLY inventory. Scans the three sources, writes reports next to this repo.
REM Edit the paths below if yours differ. Output must NOT be inside a scanned folder.
set "REPO=%~dp0..\.."
set "OUT=%REPO%\reports\phase1\windows_%DATE:~-4%%DATE:~4,2%%DATE:~7,2%"
python "%~dp0inventory.py" ^
  --root "standalone_gui=D:\GitHub\Codex-Powershell_GUI" ^
  --root "engine=C:\Users\David\Documents\faiththruphysics.com\00_SYSTEM\01_SYSTEM_OS\00_VAULT\02_CONTROL\01_ENGINE" ^
  --out "%OUT%"
if errorlevel 1 (echo Inventory FAILED. & pause & exit /b 1)
python "%~dp0visualize.py" "%OUT%"
echo Reports written to: %OUT%
start "" "%OUT%\INVENTORY_REPORT.html"
pause
