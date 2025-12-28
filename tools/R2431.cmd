@echo off
setlocal

cd /d "%~dp0\.."
echo ======================================================================
echo [R2431] Artefakte Tab: auto-refresh on activate + pipeline entry
echo Root: %CD%
echo ======================================================================

python "%~dp0R2431.py"
set ERR=%ERRORLEVEL%

echo.
echo [R2431] Beendet mit Code %ERR%
pause
exit /b %ERR%
