@echo off
setlocal
set ROOT=%~dp0..
echo.
echo ======================================================================
echo [R2388] Docking Restore Fix: restore_geometry handling + main geo fallback
echo Root: %ROOT%
echo ======================================================================
python "%~dp0R2388.py"
set RC=%ERRORLEVEL%
echo.
echo [R2388] Beendet mit Code %RC%
echo.
exit /b %RC%
