@echo off
setlocal
cd /d "%~dp0\.."
py -3 -u tools\R2224.py
exit /b %ERRORLEVEL%
