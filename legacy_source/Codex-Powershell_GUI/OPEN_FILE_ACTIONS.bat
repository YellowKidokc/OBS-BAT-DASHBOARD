@echo off
setlocal
cd /d "%~dp0"
where pythonw >nul 2>nul
if errorlevel 1 goto console
start "Codex File Actions" pythonw "%~dp0file_actions_gui.py"
exit /b 0
:console
python "%~dp0file_actions_gui.py"
if errorlevel 1 pause
