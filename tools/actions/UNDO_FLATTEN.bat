@echo off
setlocal
REM Put files back where they were, using a manifest from _flatten_manifests.
REM Usage: drag the flatten_*.csv manifest onto this file.
set "MAN=%~1"
if "%MAN%"=="" set /p "MAN=Path to flatten_*.csv manifest: "
set "PY=python"
where python >nul 2>nul || set "PY=py"
%PY% "%~dp0flatten.py" --undo "%MAN%"
if errorlevel 1 (pause & exit /b 1)
set /p "OK=Type YES to restore: "
if /i not "%OK%"=="YES" (echo Cancelled. & pause & exit /b 0)
%PY% "%~dp0flatten.py" --undo "%MAN%" --apply
pause
