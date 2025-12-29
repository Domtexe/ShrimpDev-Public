@echo off
setlocal

cd /d "%~dp0\.."
echo ======================================================================
echo [R2691] Private Push SAFE (docs-only, no git add -A)
echo Root: %CD%
echo ======================================================================

python "%~dp0R2412.py"
set ERR=%ERRORLEVEL%

echo.
echo [R2691] Beendet mit Code %ERR%
exit /b %ERR%
