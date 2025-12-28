@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2833.py"
exit /b %ERRORLEVEL%
