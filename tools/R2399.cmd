@echo off
setlocal
cd /d "%~dp0\.."

echo.
echo ======================================================================
echo [R2399] PIPELINE: offene Notizen (INI-SingleWriter, Restart-Sensitiv, Docking-Komplexitaet)
echo Root: %cd%
echo ======================================================================

py -3 tools\R2399.py
set RC=%ERRORLEVEL%

echo.
echo [R2399] Beendet mit Code %RC%
echo.
pause
exit /b %RC%
