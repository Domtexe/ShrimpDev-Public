@echo off
setlocal
cd /d "%~dp0\.."
echo.
echo ======================================================================
echo [R2390] Crash-Recovery: restore last good backups (module_docking + artefakte tab)
echo Root: %cd%
echo ======================================================================
python tools\R2390.py
set rc=%errorlevel%
echo.
echo [R2390] Beendet mit Code %rc%
echo.
exit /b %rc%
