@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2824.py" "%ROOT%"
exit /b %ERRORLEVEL%
