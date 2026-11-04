@echo off
setlocal
REM Go / no-go before handing a repo to an AI.
REM Read-only. Report saved to USERPROFILE\VaultOps\reports\repo_ready\ and opened.
set "PY=python"
where python >nul 2>nul || set "PY=py"
set "ARG=%~1"
if "%ARG%"=="" set /p "ARG=Repo folder (Enter = current folder): "
if "%ARG%"=="" set "ARG=%CD%"
%PY% "%~dp0repo_ready.py" "%ARG%" %2 %3
if defined VAULTOPS_HOME (set "R=%VAULTOPS_HOME%") else (set "R=%USERPROFILE%\VaultOps")
start "" "%R%\reports\repo_ready\repo_ready_LATEST.md"
pause
