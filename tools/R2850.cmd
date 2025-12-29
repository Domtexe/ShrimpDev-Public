@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2850.py"
exit /b %ERRORLEVEL%
