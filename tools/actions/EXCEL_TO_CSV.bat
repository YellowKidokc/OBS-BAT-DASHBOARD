@echo off
REM Excel workbook(s) -> one CSV per sheet, kept together as a book folder.
call "%~dp0_convert.bat" excel2csv "%~1"
