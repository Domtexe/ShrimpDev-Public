@echo off
setlocal
cd /d "%~dp0\.."
echo.
echo ======================================================================
echo [R2394] READ-ONLY Scan: ui_runner_products_tab builder + Toplevel/Center lines
echo Root: %cd%
echo ======================================================================
python tools\R2394.py
set rc=%errorlevel%
echo.
echo [R2394] Beendet mit Code %rc%
echo.
exit /b %rc%
