@echo off
setlocal enableextensions enabledelayedexpansion
cd /d "%~dp0\.."
echo [R1178j] FixDevIntake Runner...

rem sicheres Python-Cmd einsetzen (kein %PY% Platzhalter)
set PY=py -3 -u

rem 1) Python-Runner ausführen
%PY% tools\Runner_1178j_FixDevIntake.py
set RC=%ERRORLEVEL%
echo [R1178j] Python rc=%RC%

if %RC% NEQ 0 (
  echo [R1178j] Abbruch wegen Fehler (rc=%RC%). Siehe debug_output.txt.
  goto :end
)

rem 2) GUI starten
if exist tools\Start_MainGui.bat (
  call tools\Start_MainGui.bat
) else (
  echo [R1178j] Starte main_gui.py direkt...
  %PY% main_gui.py
)

:end
exit /b %RC%
