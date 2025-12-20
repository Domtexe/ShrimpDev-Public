@echo off
setlocal
cd /d "%~dp0\.."

echo.
echo ======================================================================
echo [R2397] PIPELINE: Docking resolved eintragen + Backlog (Quelle kopieren)
echo Root: %cd%
echo ======================================================================

py -3 tools\R2397.py
set RC=%ERRORLEVEL%

echo.
echo [R2397] Beendet mit Code %RC%
echo.
pause
exit /b %RC%
