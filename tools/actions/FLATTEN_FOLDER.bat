@echo off
setlocal
REM Flatten a folder: move files up from all subfolders, then remove the folders
REM left completely empty. Choose Here or In-house. Preview first, then YES.
call "%~dp0_mode_select.bat" "%~1"
if "%WORKDIR%"=="" (pause & exit /b 1)
%PY% "%~dp0flatten.py" "%WORKDIR%"
if errorlevel 1 (pause & exit /b 1)
echo.
set /p "OK=Type YES to do it for real: "
if /i not "%OK%"=="YES" (echo Cancelled. Nothing changed. & pause & exit /b 0)
%PY% "%~dp0flatten.py" "%WORKDIR%" --apply
start "" "%WORKDIR%"
pause
