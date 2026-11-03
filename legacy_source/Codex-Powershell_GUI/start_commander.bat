@echo off
REM Codex Script Hub - Windows Startup Script
REM This script launches the PySide6 script hub GUI application

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

REM Check if Python is available
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Python not found. Please install Python 3.8 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if PySide6 is installed
python -c "import PySide6" >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing required dependencies...
    pip install -r "%SCRIPT_DIR%requirements.txt"
)

REM Launch the application
echo Starting Codex Script Hub...
cd /d "%SCRIPT_DIR%"
start "" pythonw powershell_commander.py

REM If pythonw fails (not available), try python
if %ERRORLEVEL% NEQ 0 (
    python powershell_commander.py
)
