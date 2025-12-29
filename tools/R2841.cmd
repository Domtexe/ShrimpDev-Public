@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2841.py"
exit /b %ERRORLEVEL%
