@echo off
setlocal

cd /d "%~dp0\.."
echo ======================================================================
echo [R2433] SAFE PATCH: Artefakte tab auto-refresh on activation (compile-checked)
echo Root: %CD%
echo ======================================================================

python "%~dp0R2433.py"
set ERR=%ERRORLEVEL%

echo.
echo [R2433] Beendet mit Code %ERR%
pause
exit /b %ERR%
