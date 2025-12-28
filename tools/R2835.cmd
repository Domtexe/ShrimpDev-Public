@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2835.py"
exit /b %ERRORLEVEL%
