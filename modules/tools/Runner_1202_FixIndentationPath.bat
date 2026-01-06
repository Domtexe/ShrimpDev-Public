@echo off
setlocal
echo [R1202] FixIndentationPath...
py -3 -u "%~dp0Runner_1202_FixIndentationPath.py"
if errorlevel 1 (
  echo [R1202] FAILED. See ..\debug_output.txt
) else (
  echo [R1202] Done. Launching Main GUI...
  call "%~dp0Start_MainGui.bat"
)
endlocal
