@echo off
setlocal
cd /d "%~dp0\.."

echo.
echo ======================================================================
echo [R2396] DOCS: Docking-Fix dokumentieren (Architecture + Docking + Incident)
echo Root: %cd%
echo ======================================================================

py -3 tools\R2396.py
set RC=%ERRORLEVEL%

echo.
echo [R2396] Beendet mit Code %RC%
echo.
pause
exit /b %RC%
