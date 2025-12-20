@echo off
setlocal
echo [R1231] Intake_MinimalFixes starting...

py -3 -u "%~dp0Runner_1231_Intake_MinimalFixes.py"
if errorlevel 1 (
  echo [R1231] FAILED. See debug_output.txt
  exit /b 1
) else (
  echo [R1231] Done. rc=0
)
