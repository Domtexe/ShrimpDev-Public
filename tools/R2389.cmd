@echo off
setlocal
cd /d "%~dp0\.."
echo.
echo ======================================================================
echo [R2389] Guard UI centering after Docking restore
echo Root: %cd%
echo ======================================================================
python tools\R2389.py
set rc=%errorlevel%
echo.
echo [R2389] Beendet mit Code %rc%
exit /b %rc%
