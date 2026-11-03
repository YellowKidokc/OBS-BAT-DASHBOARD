@echo off
:: ============================================================
::  CDCM Adversarial Paper Review — RUN
::  Drop your paper (.md, .txt, .pdf) into input/ first.
:: ============================================================
cd /d "%~dp0"

if not exist config.txt (
    echo.
    echo  ERROR: config.txt not found.
    echo  Copy config.example.txt to config.txt and add your API key.
    echo.
    pause
    exit /b 1
)

if not exist input\ (
    mkdir input
)

:: Count files in input
set count=0
for %%f in (input\*) do set /a count+=1

if %count%==0 (
    echo.
    echo  ERROR: No files in input\
    echo  Drop your paper there first.
    echo.
    pause
    exit /b 1
)

echo.
echo  Starting CDCM Adversarial Review...
echo  (gpt-4o, 44 criteria, structured output)
echo.

python review_paper.py

echo.
pause
