@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2855.py"
exit /b %ERRORLEVEL%
