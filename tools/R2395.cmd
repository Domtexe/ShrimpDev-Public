@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0.."

echo.
echo ======================================================================
echo [R2395] Docking Restore: respect open=0 + prefer key.geometry (no center)
echo Root: %cd%
echo ======================================================================

py -3 tools\R2395.py
set RC=%ERRORLEVEL%

echo.
echo [R2395] Beendet mit Code %RC%
echo.
pause
exit /b %RC%
