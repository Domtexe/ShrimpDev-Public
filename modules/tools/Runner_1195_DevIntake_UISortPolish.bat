@echo off
setlocal
echo [R1195] DevIntake: UI Sort & Polish...
py -3 -u "%~dp0Runner_1195_DevIntake_UISortPolish.py"
if errorlevel 1 (
  echo [R1195] FAILED. Siehe debug_output.txt
  exit /b 1
)
call "%~dp0Start_MainGui.bat"
exit /b 0
