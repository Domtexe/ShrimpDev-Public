@echo off
setlocal
cd /d "%~dp0\.."
echo.
echo ======================================================================
echo [R2386] Docking Close Semantics: close => open=0 + remove from _wins
echo Root: %cd%
echo ======================================================================
python tools\R2386.py
set rc=%errorlevel%
echo.
echo [R2386] Beendet mit Code %rc%
exit /b %rc%
