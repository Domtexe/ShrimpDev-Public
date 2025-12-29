@echo off
setlocal
cd /d "%~dp0.."

set PY=python
%PY% tools\R2870.py
exit /b %ERRORLEVEL%
