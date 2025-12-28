@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2820.py" "%ROOT%"
exit /b %ERRORLEVEL%
