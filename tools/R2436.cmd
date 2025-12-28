@echo off
setlocal

cd /d "%~dp0\.."
echo ======================================================================
echo [R2436] Workspace API: modules/workspace_registry.py (READ-ONLY)
echo Root: %CD%
echo ======================================================================

python "%~dp0R2436.py"
set ERR=%ERRORLEVEL%

echo.
echo [R2436] Beendet mit Code %ERR%
pause
exit /b %ERR%
