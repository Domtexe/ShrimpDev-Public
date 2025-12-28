@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2832.py"
exit /b %ERRORLEVEL%
