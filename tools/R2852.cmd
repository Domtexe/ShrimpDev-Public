@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2852.py"
exit /b %ERRORLEVEL%
