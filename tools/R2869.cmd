@echo off
setlocal
cd /d "%~dp0.."

set "PY=python"
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"

"%PY%" "tools\R2869.py"
set "EC=%ERRORLEVEL%"
echo.
echo [R2869] Exit Code: %EC%
exit /b %EC%
