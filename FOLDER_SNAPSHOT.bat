@echo off
setlocal
where py >nul 2>nul
if errorlevel 1 (
  echo Python 3 is required. Install Python with the Windows Python launcher.
  pause
  exit /b 1
)
if "%~1"=="" (
  echo Drag a vault folder onto this launcher.
  echo Reports are saved under your local application data, outside the vault.
  pause
  exit /b 1
)
set "SNAPSHOT_REPORT=%LOCALAPPDATA%\ObsidianVaultDashboard\snapshots\%RANDOM%-%RANDOM%"
py -3 "%~dp0tools\folder_snapshot.py" "%~1" --output "%SNAPSHOT_REPORT%" --open
set "SNAPSHOT_EXIT=%ERRORLEVEL%"
if not "%SNAPSHOT_EXIT%"=="0" pause
exit /b %SNAPSHOT_EXIT%
