@echo off
REM ═══════════════════════════════════════════════
REM FLATTEN FOLDERS — Pull all subfolders to one level
REM 
REM Takes a deeply nested folder structure and copies
REM every folder (with its files) to a single flat output.
REM 
REM Before:  root/A/B/C/file.html  (3 levels deep)
REM After:   output/C/file.html    (1 level, folder name preserved)
REM
REM If two folders have the same name, adds _2, _3 etc.
REM
REM Usage: flatten_folders.bat "D:\path\to\source" "D:\path\to\output"
REM ═══════════════════════════════════════════════

setlocal enabledelayedexpansion

set "SOURCE=%~1"
set "OUTPUT=%~2"

if "%SOURCE%"=="" (
    echo Usage: flatten_folders.bat "source_path" "output_path"
    exit /b 1
)
if "%OUTPUT%"=="" (
    echo Usage: flatten_folders.bat "source_path" "output_path"
    exit /b 1
)

echo ═══════════════════════════════════════
echo FLATTEN FOLDERS
echo Source: %SOURCE%
echo Output: %OUTPUT%
echo ═══════════════════════════════════════

if not exist "%OUTPUT%" mkdir "%OUTPUT%"

REM Walk every directory that contains at least one file
for /r "%SOURCE%" %%D in (.) do (
    REM Count files in this specific folder (not subfolders)
    set "hasfiles=0"
    for %%F in ("%%D\*.*") do (
        if not "%%~aF"=="d" set "hasfiles=1"
    )
    
    if !hasfiles!==1 (
        REM Get just the folder name
        set "foldername=%%~nxD"
        
        REM Skip the dot
        if not "!foldername!"=="." (
            REM Check if output folder already exists
            set "target=%OUTPUT%\!foldername!"
            if exist "!target!" (
                set /a count=2
                :findname
                if exist "!target!_!count!" (
                    set /a count+=1
                    goto findname
                )
                set "target=!target!_!count!"
            )
            
            echo Copying: !foldername! -^> !target!
            xcopy "%%D\*.*" "!target!\" /Y /Q >nul 2>&1
        )
    )
)

echo.
echo ═══════════════════════════════════════
echo DONE. All folders flattened to: %OUTPUT%
echo ═══════════════════════════════════════
pause