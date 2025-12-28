@echo off
setlocal
cd /d "%~dp0\.."
py -3 -u tools\R2218.py
exit /b %ERRORLEVEL%
