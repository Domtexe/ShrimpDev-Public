@echo off
setlocal
cd /d "%~dp0\.."

echo.
echo ======================================================================
echo [R2403] PATCH: ui_toolbar INI writes -> ConfigManager (merge/SingleWriter)
echo Root: %cd%
echo ======================================================================

py -3 tools\R2403.py
set RC=%ERRORLEVEL%

echo.
echo [R2403] Beendet mit Code %RC%
echo.
pause
exit /b %RC%
