@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
echo [R1225] IntakeCore_RepairAndIntegrate starting...

REM Python 3 bevorzugt
set PY=py -3
%PY% -u "%~dp0Runner_1225_IntakeCore_RepairAndIntegrate.py"
if errorlevel 1 (
  echo [R1225] FAILED. See ..\debug_output.txt
  exit /b 1
)

REM GUI starten (optional)
if exist "%~dp0Start_MainGui.bat" (
  call "%~dp0Start_MainGui.bat"
)

echo [R1225] Done.
exit /b 0
