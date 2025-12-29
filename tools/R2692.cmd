@echo off
setlocal EnableExtensions

cd /d "%~dp0"
cd /d ".."
set "ROOT=%CD%"

echo ======================================================================
echo [R2692] Wrapper Autopush Public
echo Root: %ROOT%
echo ======================================================================

python "%~dp0R2692.py" --root "%ROOT%"
set ERR=%ERRORLEVEL%
echo.
echo [R2692] Beendet mit Code %ERR%
exit /b %ERR%
