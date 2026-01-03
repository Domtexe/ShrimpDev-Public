@echo off
setlocal
title [R1190] DevIntake Install
echo [R1190] Installing Dev-Intake (clean)...
py -3 -u "%~dp0Runner_1190_DevIntake_Install.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [R1190] FAILED (rc=%rc%). See debug_output.txt.
  exit /b %rc%
)
echo [R1190] OK. Launching Main GUI...
call "%~dp0Start_MainGui.bat"
exit /b 0
