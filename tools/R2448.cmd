@echo off
setlocal
cd /d "%~dp0.."
echo ======================================================================
echo [R2448] UI: Purge buttons enable/disable + top-right alignment padding
echo Root: %cd%
echo ======================================================================
python tools\R2448.py
set RC=%ERRORLEVEL%
echo.
echo [R2448] Beendet mit Code %RC%
exit /b %RC%
