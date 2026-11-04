@echo off
setlocal
REM How messy is this folder: exact duplicates and wasted space.
REM Read-only. Report saved to USERPROFILE\VaultOps\reports\duplicate_report\ and opened.
set "PY=python"
where python >nul 2>nul || set "PY=py"
set "ARG=%~1"
if "%ARG%"=="" set /p "ARG=Folder (Enter = current folder): "
if "%ARG%"=="" set "ARG=%CD%"
%PY% "%~dp0duplicate_report.py" "%ARG%" 
if defined VAULTOPS_HOME (set "R=%VAULTOPS_HOME%") else (set "R=%USERPROFILE%\VaultOps")
start "" "%R%\reports\duplicate_report\duplicate_report_LATEST.md"
pause
