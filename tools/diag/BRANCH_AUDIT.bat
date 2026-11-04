@echo off
setlocal
REM Which branches landed, which are floating, across all repos in a folder.
REM Read-only. Report saved to USERPROFILE\VaultOps\reports\branch_audit\ and opened.
set "PY=python"
where python >nul 2>nul || set "PY=py"
set "ARG=%~1"
if "%ARG%"=="" set /p "ARG=Repos folder (Enter = D:\GitHub): "
if "%ARG%"=="" set "ARG=D:\GitHub"
%PY% "%~dp0branch_audit.py" "%ARG%" 
if defined VAULTOPS_HOME (set "R=%VAULTOPS_HOME%") else (set "R=%USERPROFILE%\VaultOps")
start "" "%R%\reports\branch_audit\branch_audit_LATEST.md"
pause
