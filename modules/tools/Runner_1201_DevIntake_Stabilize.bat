@echo off
setlocal
title [R1201] DevIntake Stabilize
echo [R1201] Starting DevIntake Stabilize...
pushd "%~dp0"
for %%I in ("%~dp0.") do set ROOT=%%~dpI
set ROOT=%ROOT:~0,-1%
rem ^-- %ROOT% zeigt auf D:\ShrimpDev\tools

py -3 -u "%~dp0Runner_1201_DevIntake_Stabilize.py"
if errorlevel 1 (
  echo [R1201] FAILED. Siehe ..\debug_output.txt
) else (
  echo [R1201] OK. Starte Main GUI...
  call "%~dp0Start_MainGui.bat"
)
endlocal
