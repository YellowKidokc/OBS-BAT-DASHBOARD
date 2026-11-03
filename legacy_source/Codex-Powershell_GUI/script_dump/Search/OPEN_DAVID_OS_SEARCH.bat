@echo off
setlocal
set "DAVID_OS_ROOT=D:\GitHub\David-OSv3"
set "SEARCH_LAUNCHER=%DAVID_OS_ROOT%\gui\START_DAVID_OS_SEARCH.bat"

if not exist "%SEARCH_LAUNCHER%" (
  echo David OS Search was not found at:
  echo   %SEARCH_LAUNCHER%
  echo.
  echo Update DAVID_OS_ROOT near the top of this launcher if the repository moved.
  pause
  exit /b 1
)

call "%SEARCH_LAUNCHER%"
if errorlevel 1 pause
