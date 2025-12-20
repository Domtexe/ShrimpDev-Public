@echo off
setlocal
cd /d "%~dp0\.."
echo.
echo ======================================================================
echo [R2387] READ-ONLY Diagnose: Docking section presence + who writes INI
echo Root: %cd%
echo ======================================================================
python tools\R2387.py
set rc=%errorlevel%
echo.
echo [R2387] Beendet mit Code %rc%
exit /b %rc%
