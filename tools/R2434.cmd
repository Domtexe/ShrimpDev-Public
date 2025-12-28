@echo off
setlocal

cd /d "%~dp0\.."
echo ======================================================================
echo [R2434] PIPELINE: Add GitHub update urgency indicator task (P1)
echo Root: %CD%
echo ======================================================================

python "%~dp0R2434.py"
set ERR=%ERRORLEVEL%

echo.
echo [R2434] Beendet mit Code %ERR%
pause
exit /b %ERR%
