@echo off
:: ============================================================
::  YAML-COPILOT (Two-Step)
:: ============================================================
title YAML-COPILOT Two-Step
cd /d "%~dp0"

echo.
echo ============================================================
echo   YAML-COPILOT Two-Step
echo ============================================================
echo.
echo   1. Edit config.txt (API key + model)
echo   2. Drop markdown files into input\
echo   3. Run this script
echo.
echo ============================================================
echo.

where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    pause
    exit /b 1
)

python -c "import openai" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing OpenAI Python package ...
    pip install openai
    echo.
)

python "%~dp0two_step_yaml_copilot.py"

echo.
echo ============================================================
echo   Done! Check output\ for STEP1 json and YAML outputs.
echo ============================================================
pause
