@echo off
setlocal

set "ROOT=%~dp0.."
python "%ROOT%\tools\R2829.py"
exit /b %ERRORLEVEL%
