@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0\.."
set "PY=py"
set "PYFLAGS=-3 -u"

echo [R1189] Repair + LEDs + Detect: starte...
"%PY%" %PYFLAGS% "tools\Runner_1189_IntakeRepairAndLEDsFix.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [R1189] FAILED (rc=%RC%). Siehe debug_output.txt
  exit /b %RC%
)

echo [R1189] OK. Launching Main GUI...
if exist "tools\Start_MainGui.bat" (
  call "tools\Start_MainGui.bat"
) else (
  "%PY%" %PYFLAGS% "main_gui.py"
)
exit /b 0
