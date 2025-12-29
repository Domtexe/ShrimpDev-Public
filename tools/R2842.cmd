@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2842.py"
exit /b %ERRORLEVEL%
