@echo off
REM Installs/checks what the conversion actions need. Safe to re-run.
set "PY=python"
where python >nul 2>nul || set "PY=py"
echo Installing Python packages (openpyxl, Microsoft MarkItDown)...
%PY% -m pip install --upgrade -r "%~dp0requirements.txt"
echo.
where pandoc >nul 2>nul && (echo pandoc: OK) || (echo pandoc: missing - installing & winget install --id JohnMacFarlane.Pandoc -e)
where typst >nul 2>nul && (echo PDF engine typst: OK) || (echo PDF engine: missing. For Markdown-to-PDF run: winget install --id Typst.Typst -e)
echo.
echo Done. Close and reopen this window if pandoc was just installed.
pause
