@echo off
setlocal
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo Python was not found. Install Python 3.10 or newer and select Add Python to PATH.
  pause
  exit /b 1
)
python -m pip install -r "%~dp0requirements.txt"
python -m py_compile script_hub.py file_actions.py file_actions_gui.py
if errorlevel 1 (
  echo Setup found a problem.
  pause
  exit /b 1
)
echo Setup and checks completed.
pause
