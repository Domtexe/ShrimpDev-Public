@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2847.py"
exit /b %ERRORLEVEL%
