@echo off
setlocal
cd /d "%~dp0\.."
echo.
echo ======================================================================
echo [R2393] PATCH: ui_runner_products_tab builder must not create its own Toplevel
echo Root: %cd%
echo ======================================================================
python tools\R2393.py
set rc=%errorlevel%
echo.
echo [R2393] Beendet mit Code %rc%
echo.
exit /b %rc%
