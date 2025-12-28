@echo off
setlocal
set "ROOT=%~dp0.."
python "%ROOT%\tools\R2812.py" "%ROOT%"
exit /b %ERRORLEVEL%
