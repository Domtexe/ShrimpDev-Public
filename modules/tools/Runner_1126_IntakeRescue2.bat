@echo off
setlocal
cd /d "%~dp0\.."
set PY=py -3
%PY% "tools\Runner_1126_IntakeRescue2.py"
set RC=%ERRORLEVEL%
echo [R1126] RC=%RC%
exit /b %RC%
