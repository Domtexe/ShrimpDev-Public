@echo off
setlocal
echo [R1221] IntakeCore_Addons starting...
py -3 -u "%~dp0Runner_1221_IntakeCore_Addons.py"
if errorlevel 1 (
  echo [R1221] FAILED. See debug_output.txt
  exit /b 1
) else (
  echo [R1221] Done. rc=0
)
