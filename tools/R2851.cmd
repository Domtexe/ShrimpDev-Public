@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2851.py"
exit /b %ERRORLEVEL%
