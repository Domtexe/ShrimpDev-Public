@echo off
setlocal
echo [R1207] FixIntakeCoreSafe starting...
set PY=py -3 -u
%PY% "%~dp0Runner_1207_FixIntakeCoreSafe.py"
if errorlevel 1 (
  echo [R1207] FAILED. Siehe debug_output.txt
  exit /b 1
)
echo [R1207] OK. Launching Main GUI...
call "%~dp0Start_MainGui.bat"
exit /b 0
