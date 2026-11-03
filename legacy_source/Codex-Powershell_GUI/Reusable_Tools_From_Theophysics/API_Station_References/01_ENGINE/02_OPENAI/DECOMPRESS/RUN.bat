@echo off
echo ========================================
echo   LOSSLESS DECOMPRESSOR
echo ========================================
echo.

if "%~1"=="" (
    echo Usage: RUN.bat input_file.md
    echo.
    echo Example: RUN.bat LOSSLESS_188.md
    echo.
    pause
    exit /b 1
)

python run_decompressor.py "%~1"
pause
