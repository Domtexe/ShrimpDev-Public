@echo off
setlocal
cd /d "%~dp0\.."
echo [R1199] Starting IntakeHotfix...
py -3 -u "tools\Runner_1199_IntakeHotfix.py"
if errorlevel 1 (
  echo [R1199] FAILED. See debug_output.txt
  exit /b 1
)
echo [R1199] OK. Launching Main GUI...
call "tools\Start_MainGui.bat"
exit /b 0
