@echo off
setlocal
cd /d "%~dp0\.."
echo.
echo ======================================================================
echo [R2391] Syntax Emergency Restore (module_docking + ui_runner_products_tab)
echo Root: %cd%
echo ======================================================================
python tools\R2391.py
set rc=%errorlevel%
echo.
echo [R2391] Beendet mit Code %rc%
exit /b %rc%
