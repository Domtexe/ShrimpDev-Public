@echo off
setlocal
echo [R1194] DevIntake: UI-Arrange (ohne Filter, gruppierte Toolbars, LEDs mit Label)...
set TOOLS=%~dp0
py -3 -u "%~dp0Runner_1194_DevIntake_UIArrange.py"
if errorlevel 1 (
  echo [R1194] FAILED. Siehe debug_output.txt
  exit /b 1
)
call "%~dp0Start_MainGui.bat"
exit /b 0
