@echo off
setlocal
cd /d "%~dp0\.."
echo.
echo ======================================================================
echo [R2382] Patch config_manager.py -> save() delegates to ini_writer (SingleWriter)
echo Root: %cd%
echo ======================================================================
python tools\R2382.py
set rc=%errorlevel%
echo.
echo [R2382] Beendet mit Code %rc%
exit /b %rc%
