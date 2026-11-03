@echo off
setlocal
cd /d "%~dp0"
echo Codex Powershell GUI - Troubleshooter
echo Repository: %CD%
echo.
where python
python --version
python -c "import PySide6; print('PySide6: OK')"
python -c "import openpyxl; print('openpyxl: OK')"
python -m py_compile script_hub.py file_actions.py file_actions_gui.py
echo.
echo If a dependency is missing, run SETUP_OR_REPAIR.bat.
pause
