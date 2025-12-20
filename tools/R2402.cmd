@echo off
setlocal
cd /d "%~dp0\.."

echo.
echo ======================================================================
echo [R2402] PATCH: Delegate config_loader.save/config_mgr.save -> config_manager (SingleWriter path)
echo Root: %cd%
echo ======================================================================

py -3 tools\R2402.py
set RC=%ERRORLEVEL%

echo.
echo [R2402] Beendet mit Code %RC%
echo.
pause
exit /b %RC%
