@echo off
setlocal
cd /d "%~dp0\.."
echo.
echo ======================================================================
echo [R2392] READ-ONLY Scan: Toplevel/Centers in tab builders (Docking conflict)
echo Root: %cd%
echo ======================================================================
python tools\R2392.py
set rc=%errorlevel%
echo.
echo [R2392] Beendet mit Code %rc%
echo.
exit /b %rc%
