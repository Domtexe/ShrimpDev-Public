@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2822.py" "%ROOT%"
exit /b %ERRORLEVEL%
