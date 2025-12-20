@echo off
setlocal
title [R1198] Intake LED Fix
echo [R1198] Starting IntakeLedFix...

REM Starte Python-Runner
py -3 -u "tools\Runner_1198_IntakeLedFix.py"
if errorlevel 1 (
  echo [R1198] FAILED. See debug_output.txt.
  exit /b 1
)

echo [R1198] OK. Launching Main GUI...
call "tools\Start_MainGui.bat"
exit /b 0
