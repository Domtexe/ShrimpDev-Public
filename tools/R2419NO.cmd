@echo off
setlocal

cd /d "%~dp0\.."
echo ======================================================================
echo [R2419] UI Fix: Force top-edge padding (row_push/outer pack)
echo Root: %CD%
echo ======================================================================

python "%~dp0R2419.py"
set ERR=%ERRORLEVEL%

echo.
echo [R2419] Beendet mit Code %ERR%
pause
exit /b %ERR%
