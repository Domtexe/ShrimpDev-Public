@echo off
setlocal
cd /d "%~dp0\.."

echo.
echo ======================================================================
echo [R2398] SNAPSHOT: Docking-stabil (modules + docs + ShrimpDev.ini)
echo Root: %cd%
echo ======================================================================

py -3 tools\R2398.py
set RC=%ERRORLEVEL%

echo.
echo [R2398] Beendet mit Code %RC%
echo.
pause
exit /b %RC%
