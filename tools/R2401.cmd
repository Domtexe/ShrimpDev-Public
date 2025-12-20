@echo off
setlocal
cd /d "%~dp0\.."

echo.
echo ======================================================================
echo [R2401] READ-ONLY: INI Writer Deep Scan (config_loader/config_mgr/ui_toolbar)
echo Root: %cd%
echo ======================================================================

py -3 tools\R2401.py
set RC=%ERRORLEVEL%

echo.
echo [R2401] Beendet mit Code %RC%
echo.
pause
exit /b %RC%
