@echo off
setlocal

cd /d "%~dp0\.."
echo ======================================================================
echo [R2692] Public Whitelist Sync (Private -> Public) + commit + push
echo Root: %CD%
echo ======================================================================

python "%~dp0R2411.py"
set ERR=%ERRORLEVEL%

echo.
echo [R2692] Beendet mit Code %ERR%
exit /b %ERR%
