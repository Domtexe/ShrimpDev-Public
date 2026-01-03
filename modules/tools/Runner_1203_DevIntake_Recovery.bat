@echo off
setlocal
cd /d "%~dp0\.."
echo [R1203] Running DevIntake_Recovery...
py -3 -u "tools\Runner_1203_DevIntake_Recovery.py"
if errorlevel 1 (
  echo [R1203] FAILED. See ..\debug_output.txt
  exit /b 1
)
echo [R1203] OK. Launching Main GUI...
call tools\Start_MainGui.bat
endlocal
