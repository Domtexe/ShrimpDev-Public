@echo off
setlocal

cd /d "%~dp0\.."
echo ======================================================================
echo [R2429] UI Layout Fix: Top-right align Push/Purge; Row1 left above tree
echo Root: %CD%
echo ======================================================================

python "%~dp0R2429.py"
set ERR=%ERRORLEVEL%

echo.
echo [R2429] Beendet mit Code %ERR%
pause
exit /b %ERR%
