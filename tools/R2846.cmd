@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2846.py"
exit /b %ERRORLEVEL%
