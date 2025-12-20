@echo off
setlocal
cd /d "%~dp0\.."

echo.
echo ======================================================================
echo [R2406] PATCH: Apply main geometry from [Docking] main.geometry on startup
echo Root: %cd%
echo ======================================================================

py -3 tools\R2406.py
set RC=%ERRORLEVEL%

echo.
echo [R2406] Beendet mit Code %RC%
echo.
pause
exit /b %RC%
