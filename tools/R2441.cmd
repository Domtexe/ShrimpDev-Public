@echo off
setlocal

cd /d "%~dp0\.."
echo ======================================================================
echo [R2441] Workspace Dropdown (indent-safe) + compile-check + rollback
echo Root: %CD%
echo ======================================================================

python "%~dp0R2441.py"
set ERR=%ERRORLEVEL%

echo.
echo [R2441] Beendet mit Code %ERR%
pause
exit /b %ERR%
