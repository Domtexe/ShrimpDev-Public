@echo off
setlocal
cd /d "%~dp0\.."

echo.
echo ======================================================================
echo [R2404] READ-ONLY: Post-Restore Geometry Setter Scan (who centers/drifts?)
echo Root: %cd%
echo ======================================================================

py -3 tools\R2404.py
set RC=%ERRORLEVEL%

echo.
echo [R2404] Beendet mit Code %RC%
echo.
pause
exit /b %RC%
