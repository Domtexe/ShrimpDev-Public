@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2834.py"
exit /b %ERRORLEVEL%
