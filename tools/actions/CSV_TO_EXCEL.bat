@echo off
REM CSV(s) -> Excel. A book folder from EXCEL_TO_CSV rebuilds the same workbook.
call "%~dp0_convert.bat" csv2excel "%~1"
