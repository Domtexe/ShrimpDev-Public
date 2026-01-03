@echo off
setlocal
echo [R1218] FixIntake_NewlineSafe starting...
py -3 -u "%~dp0Runner_1218_FixIntake_NewlineSafe.py"
if errorlevel 1 (
  echo [R1218] FAILED. See debug_output.txt
  exit /b 1
) else (
  echo [R1218] Done. rc=0
)
