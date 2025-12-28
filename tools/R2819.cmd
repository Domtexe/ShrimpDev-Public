@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2819.py" "%ROOT%"
exit /b %ERRORLEVEL%
