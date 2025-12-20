@echo off
setlocal
title [R1209] IntakePathFinalFix
cd /d "%~dp0"
echo [R1209] Starting IntakePathFinalFix...
py -3 -u "%~dp0Runner_1209_IntakePathFinalFix.py"
if errorlevel 1 (
  echo [R1209] FAILED. Siehe ..\debug_output.txt
  exit /b 1
)
echo [R1209] OK. Launching GUI...
call "%~dp0Start_MainGui.bat"
exit /b 0
