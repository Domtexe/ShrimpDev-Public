@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2828.py"
exit /b %ERRORLEVEL%
