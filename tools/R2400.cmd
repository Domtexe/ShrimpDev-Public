@echo off
setlocal
cd /d "%~dp0\.."

echo.
echo ======================================================================
echo [R2400] READ-ONLY: Remaining INI Writers Map (ShrimpDev.ini write paths)
echo Root: %cd%
echo ======================================================================

py -3 tools\R2400.py
set RC=%ERRORLEVEL%

echo.
echo [R2400] Beendet mit Code %RC%
echo.
pause
exit /b %RC%
