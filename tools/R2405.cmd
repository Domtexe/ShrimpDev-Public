@echo off
setlocal
cd /d "%~dp0\.."

echo.
echo ======================================================================
echo [R2405] PATCH: Pipeline updaten (offene Punkte einsortieren, Dupe-Schutz)
echo Root: %cd%
echo ======================================================================

py -3 tools\R2405.py
set RC=%ERRORLEVEL%

echo.
echo [R2405] Beendet mit Code %RC%
echo.
pause
exit /b %RC%
