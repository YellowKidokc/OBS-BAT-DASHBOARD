@echo off
REM Codex Script Hub - Remove from Windows Startup

echo ==============================================
echo Codex Script Hub - Remove from Startup
echo ==============================================
echo.

set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
set SHORTCUT_PATH=%STARTUP_FOLDER%\Codex Script Hub.lnk

if exist "%SHORTCUT_PATH%" (
    del "%SHORTCUT_PATH%"
    echo SUCCESS! Codex Script Hub removed from startup.
) else (
    echo Codex Script Hub was not in startup.
)

echo.
pause
