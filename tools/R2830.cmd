@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2830.py"
exit /b %ERRORLEVEL%
