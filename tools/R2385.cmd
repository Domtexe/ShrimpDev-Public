@echo off
setlocal
cd /d "%~dp0\.."
echo.
echo ======================================================================
echo [R2385] Docking Persist: persist_all on Restart + on App-Close (safe)
echo Root: %cd%
echo ======================================================================
python tools\R2385.py
set rc=%errorlevel%
echo.
echo [R2385] Beendet mit Code %rc%
exit /b %rc%
