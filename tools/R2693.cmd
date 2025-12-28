@echo off
setlocal EnableExtensions

cd /d "%~dp0"
cd /d ".."
set "ROOT=%CD%"

echo ======================================================================
echo [R2693] Wrapper Autopush BOTH
echo Root: %ROOT%
echo ======================================================================

python "%~dp0R2693.py" --root "%ROOT%"
set ERR=%ERRORLEVEL%
echo.
echo [R2693] Beendet mit Code %ERR%
exit /b %ERR%
