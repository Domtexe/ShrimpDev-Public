@echo off
setlocal ENABLEDELAYEDEXPANSION
title [1174j] IntakeRestoreSmartFix

pushd "%~dp0\.."
set ROOT=%CD%
echo [1174j] Starte IntakeRestoreSmartFix...
set PY=py -3 -u

%PY% tools\Runner_1174j_IntakeRestoreSmartFix.py
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [1174j] FEHLER: Python-Runner RC=%RC%.
  goto :EOF
)

echo [1174j] OK. Starte jetzt testweise Haupt-GUI:
echo        %PY% main_gui.py
popd
exit /b 0
