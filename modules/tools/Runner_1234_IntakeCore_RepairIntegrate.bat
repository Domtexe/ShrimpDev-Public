@echo off
setlocal enabledelayedexpansion
title [R1234] IntakeCore Repair & Integrate

cd /d "%~dp0"
cd ..

set PY=py -3 -u
echo [R1234] Starting IntakeCore_RepairIntegrate...
%PY% tools\Runner_1234_IntakeCore_RepairIntegrate.py
set RC=%ERRORLEVEL%
echo [R1234] Done. rc=%RC%

if %RC% NEQ 0 (
  echo [R1234] ERROR. See debug_output.txt
  pause
  exit /b %RC%
)

echo [R1234] Launching GUI...
call tools\Start_MainGui.bat
exit /b 0
