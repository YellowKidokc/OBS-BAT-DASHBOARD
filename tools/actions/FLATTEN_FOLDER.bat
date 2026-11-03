@echo off
setlocal
REM Flatten a folder: move every file from its subfolders up into it, then remove
REM the subfolders that are left completely empty. Shows a preview first.
REM Usage: drag a folder onto this file, or run it and type/paste a path.
REM With no argument and nothing typed, it uses the folder this .bat sits in.
set "TARGET=%~1"
if "%TARGET%"=="" set /p "TARGET=Folder to flatten (Enter = this folder): "
if "%TARGET%"=="" set "TARGET=%~dp0."
set "PY=python"
where python >nul 2>nul || set "PY=py"
%PY% "%~dp0flatten.py" "%TARGET%"
if errorlevel 1 (pause & exit /b 1)
echo.
set /p "OK=Type YES to do it for real: "
if /i not "%OK%"=="YES" (echo Cancelled. Nothing changed. & pause & exit /b 0)
%PY% "%~dp0flatten.py" "%TARGET%" --apply
pause
