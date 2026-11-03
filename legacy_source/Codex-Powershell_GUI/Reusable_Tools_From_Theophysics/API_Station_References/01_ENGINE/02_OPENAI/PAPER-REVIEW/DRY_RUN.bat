@echo off
:: ============================================================
::  CDCM Adversarial Paper Review — DRY RUN (cost estimate)
::  No API call is made. Shows token count and cost estimate.
:: ============================================================
cd /d "%~dp0"
echo.
echo  DRY RUN — No API call will be made.
echo  Showing cost estimate only.
echo.
python review_paper.py --dry-run
echo.
pause
