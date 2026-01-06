@echo off
setlocal
title [R1205] FixIntakeIndentAndLEDs
echo [R1205] Running FixIntakeIndentAndLEDs...
py -3 -u "%~dp0Runner_1205_FixIntakeIndentAndLEDs.py"
if errorlevel 1 (
  echo [R1205] FAILED. See ..\debug_output.txt
  exit /b 1
)
echo [R1205] OK. Launching Main GUI...
call "%~dp0Start_MainGui.bat"
exit /b 0
