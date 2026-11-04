@echo off
REM Word, PowerPoint, Excel, PDF, HTML, EPUB, CSV, JSON... -> Markdown (Microsoft MarkItDown).
call "%~dp0_convert.bat" tomd "%~1"
