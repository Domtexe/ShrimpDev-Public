@echo off
setlocal

cd /d "%~dp0\.."
echo ======================================================================
echo [R2414] Autopush BOTH: Private (R2691) -> Public (R2692)
echo Root: %CD%
echo ======================================================================

python "%~dp0R2414.py"
set ERR=%ERRORLEVEL%

echo.
echo [R2414] Beendet mit Code %ERR%
pause
exit /b %ERR%
