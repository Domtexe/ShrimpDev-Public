@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2837.py"
exit /b %ERRORLEVEL%
