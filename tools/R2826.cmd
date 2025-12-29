@echo off
setlocal

set "ROOT=%~dp0.."
python "%ROOT%\tools\R2826.py"
exit /b %ERRORLEVEL%
