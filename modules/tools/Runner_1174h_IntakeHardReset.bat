@echo off
setlocal ENABLEDELAYEDEXPANSION
title [1174h] IntakeHardReset

pushd "%~dp0\.."
set ROOT=%CD%
echo [1174h] Starte IntakeHardReset...
echo [1174h] Root  : %ROOT%

REM Python 3 launcher
set PY=py -3 -u

%PY% tools\Runner_1174h_IntakeHardReset.py
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [1174h] FEHLER: Python-Runner beendete sich mit RC=%RC%.
  goto :EOF
)

echo [1174h] OK. Du kannst jetzt starten mit:
echo         %PY% main_gui.py
popd
exit /b 0
