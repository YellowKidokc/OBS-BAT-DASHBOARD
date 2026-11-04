@echo off
setlocal
REM What changed in the vault since the last pulse / last 24 hours.
REM Read-only. Report saved to USERPROFILE\VaultOps\reports\vault_pulse\ and opened.
set "PY=python"
where python >nul 2>nul || set "PY=py"
set "ARG=%~1"
if "%ARG%"=="" set /p "ARG=Vault folder (Enter = saved default): "
if "%ARG%"=="" set "ARG=%VAULTOPS_VAULT%"
%PY% "%~dp0vault_pulse.py" "%ARG%" 
if defined VAULTOPS_HOME (set "R=%VAULTOPS_HOME%") else (set "R=%USERPROFILE%\VaultOps")
start "" "%R%\reports\vault_pulse\vault_pulse_LATEST.md"
pause
