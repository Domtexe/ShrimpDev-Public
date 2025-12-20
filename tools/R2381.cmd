@echo off
setlocal
cd /d "%~dp0\.."
echo.
echo ======================================================================
echo [R2381] READ-ONLY Structure Scan: modules/config_manager.py (write entrypoints)
echo Root: %cd%
echo ======================================================================
python tools\R2381.py
set rc=%errorlevel%
echo.
echo [R2381] Beendet mit Code %rc%
exit /b %rc%
