@echo off
setlocal
cd /d "%~dp0\.."
echo [R1196] Installing Dev-Intake...
py -3 -u "tools\Runner_1196_DevIntake_Apply.py"
if errorlevel 1 (
  echo [R1196] FAILED.
) else (
  echo [R1196] OK. Launching Main GUI...
  call tools\Start_MainGui.bat
)
endlocal
