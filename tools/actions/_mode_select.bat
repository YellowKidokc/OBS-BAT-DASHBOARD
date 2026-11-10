@echo off
REM Shared helper: asks for a folder and a mode, sets WORKDIR for the caller.
REM   call "%~dp0_mode_select.bat" "%~1"   then use %WORKDIR% (empty = cancelled)
set "WORKDIR="
set "SRC=%~1"
if "%SRC%"=="" set /p "SRC=Folder (drag it here, Enter = this folder): "
if "%SRC%"=="" set "SRC=%CD%"
set "SRC=%SRC:"=%"
if not exist "%SRC%\" (echo Not a folder: %SRC% & exit /b 1)
set "PY=python"
where python >nul 2>nul || set "PY=py"
echo.
echo Folder: %SRC%
echo   [1] Here       - act on this folder where it is
echo   [2] In-house   - verified copy into the workspace, act on the copy (original untouched)
echo   [0] Cancel
set /p "MODE=Choose: "
if "%MODE%"=="1" (set "WORKDIR=%SRC%" & exit /b 0)
if not "%MODE%"=="2" exit /b 1
for /f "usebackq delims=" %%P in (`%PY% "%~dp0inhouse.py" "%SRC%"`) do set "WORKDIR=%%P"
if "%WORKDIR%"=="" (echo In-house copy failed. & exit /b 1)
echo Working on copy: %WORKDIR%
exit /b 0
