@echo off
setlocal ENABLEDELAYEDEXPANSION
title [1174i] IntakeRestoreSmart

pushd "%~dp0\.."
set ROOT=%CD%
echo [1174i] Starte IntakeRestoreSmart...
echo [1174i] Root  : %ROOT%

set PY=py -3 -u

%PY% tools\Runner_1174i_IntakeRestoreSmart.py
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [1174i] FEHLER: Python-Runner RC=%RC%.
  goto :EOF
)

echo [1174i] OK. Starte jetzt testweise Haupt-GUI:
echo        %PY% main_gui.py
popd
exit /b 0
