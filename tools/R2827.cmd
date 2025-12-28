@echo off
setlocal

set "ROOT=%~dp0.."
python "%ROOT%\tools\R2827.py"
exit /b %ERRORLEVEL%
