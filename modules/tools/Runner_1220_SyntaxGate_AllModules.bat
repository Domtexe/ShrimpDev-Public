@echo off
setlocal
echo [R1220] SyntaxGate_AllModules starting...
py -3 -u "%~dp0Runner_1220_SyntaxGate_AllModules.py"
if errorlevel 1 (
  echo [R1220] FAILED. See debug_output.txt
  exit /b 1
) else (
  echo [R1220] Done. rc=0
)
