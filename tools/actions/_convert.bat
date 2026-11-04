@echo off
REM Shared runner: _convert.bat ACTION "PATH" [FORMAT]
REM Shows a preview, asks for YES, writes to a new _converted folder (or the in-house workspace).
setlocal
set "ACT=%~1"
set "SRC=%~2"
set "FMT=%~3"
if "%SRC%"=="" set /p "SRC=File or folder (drag it here): "
set "SRC=%SRC:"=%"
if not exist "%SRC%" (echo Not found: %SRC% & pause & exit /b 1)
set "PY=python"
where python >nul 2>nul || set "PY=py"
set "EXTRA="
if not "%FMT%"=="" set "EXTRA=--to %FMT%"
echo.
echo Where should the results go?
echo   [1] Next to the source, in a new _converted folder
echo   [2] In-house workspace (%%USERPROFILE%%\VaultOps\WORKSPACE\converted)
set /p "MODE=Choose [1]: "
set "OUTARG="
if "%MODE%"=="2" (
  if defined VAULTOPS_WORKSPACE (set "WS=%VAULTOPS_WORKSPACE%") else (set "WS=%USERPROFILE%\VaultOps\WORKSPACE")
  for /f %%T in ('%PY% -c "import datetime;print(datetime.datetime.now().strftime('%%Y%%m%%d-%%H%%M%%S'))"') do set "STAMP=%%T"
)
if "%MODE%"=="2" set "OUTARG=--out "%WS%\converted\%ACT%_%STAMP%""
%PY% "%~dp0convert.py" %ACT% "%SRC%" %EXTRA% %OUTARG%
if errorlevel 1 (pause & exit /b 1)
echo.
set /p "OK=Type YES to convert: "
if /i not "%OK%"=="YES" (echo Cancelled. Nothing written. & pause & exit /b 0)
%PY% "%~dp0convert.py" %ACT% "%SRC%" %EXTRA% %OUTARG% --apply
pause
