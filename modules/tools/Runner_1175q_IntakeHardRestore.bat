@echo off
setlocal ENABLEDELAYEDEXPANSION
title [1175q] IntakeHardRestore

echo [1175q] IntakeHardRestore: starte Patch...
set ROOT=%~dp0..
pushd "%ROOT%"

REM Python im ShrimpDev-Kontext
set PY=py -3 -u

REM Ausführen
%PY% "tools\Runner_1175q_IntakeHardRestore.py"
if errorlevel 1 (
  echo [1175q] FEHLER. Siehe Konsole / debug_output.txt
  popd
  exit /b 1
)

echo [1175q] Patch erfolgreich, Syntax OK.
popd
exit /b 0
