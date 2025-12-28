@echo off
setlocal
cd /d "%~dp0"
python R2865.py
set EC=%ERRORLEVEL%
echo.
echo [Runner beendet mit Code %EC%]
exit /b %EC%
