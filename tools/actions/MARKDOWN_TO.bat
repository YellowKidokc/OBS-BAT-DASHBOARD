@echo off
REM Markdown -> another format (pandoc).
echo Convert Markdown to:
echo   [1] Word (.docx)   [2] Web page (.html)   [3] PDF   [4] PowerPoint (.pptx)
echo   [5] OpenDocument (.odt)   [6] Rich text (.rtf)   [7] E-book (.epub)   [8] Plain text
set /p "C=Choose: "
for %%A in ("1=docx" "2=html" "3=pdf" "4=pptx" "5=odt" "6=rtf" "7=epub" "8=txt") do for /f "tokens=1,2 delims==" %%X in (%%A) do if "%C%"=="%%X" set "FMT=%%Y"
if not defined FMT (echo Cancelled. & pause & exit /b 0)
call "%~dp0_convert.bat" frommd "%~1" %FMT%
