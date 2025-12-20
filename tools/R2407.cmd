@echo off
setlocal
cd /d "%~dp0\.."

echo.
echo ======================================================================
echo [R2407] READ-ONLY: Docking Start State Audit (INI vs runtime)
echo Root: %cd%
echo ======================================================================

py -3 tools\R2407.py
set RC=%ERRORLEVEL%

echo.
echo [R2407] Beendet mit Code %RC%
echo.
pause
exit /b %RC%
