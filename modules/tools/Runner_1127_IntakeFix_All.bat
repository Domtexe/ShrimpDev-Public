@echo off
setlocal
cd /d "%~dp0\.."
set PY=py -3
echo [R1127] IntakeFix_All - Start
%PY% -u "tools\Runner_1127_IntakeFix_All.py"
set RC=%ERRORLEVEL%
echo [R1127] Ende RC=%RC%
exit /b %RC%
