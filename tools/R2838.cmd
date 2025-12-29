@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2838.py"
exit /b %ERRORLEVEL%
