@echo off
setlocal

cd /d "%~dp0\.."
echo ======================================================================
echo [R2428] UI Gate: Push buttons enabled only when allowed (busy/order/path)
echo Root: %CD%
echo ======================================================================

python "%~dp0R2428.py"
set ERR=%ERRORLEVEL%

echo.
echo [R2428] Beendet mit Code %ERR%
pause
exit /b %ERR%
