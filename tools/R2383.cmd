@echo off
setlocal
cd /d "%~dp0\.."
echo.
echo ======================================================================
echo [R2383] READ-ONLY Docking Diagnose: auto-open / restore / center scan
echo Root: %cd%
echo ======================================================================
python tools\R2383.py
set rc=%errorlevel%
echo.
echo [R2383] Beendet mit Code %rc%
exit /b %rc%
