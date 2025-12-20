@echo off
setlocal
cd /d "%~dp0\.."
echo.
echo ======================================================================
echo [R2384] READ-ONLY Hook Scan: Docking close/restore/undock entrypoints
echo Root: %cd%
echo ======================================================================
python tools\R2384.py
set rc=%errorlevel%
echo.
echo [R2384] Beendet mit Code %rc%
exit /b %rc%
