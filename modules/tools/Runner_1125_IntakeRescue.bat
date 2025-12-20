@echo off
setlocal
cd /d "%~dp0\.."
set PY=py -3
%PY% "tools\Runner_1125_IntakeRescue.py"
set RC=%ERRORLEVEL%
echo [R1125] RC=%RC%
exit /b %RC%
