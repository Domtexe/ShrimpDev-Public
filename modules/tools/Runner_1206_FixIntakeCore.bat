@echo off
setlocal
title [R1206] Intake Core Fix
cd /d "%~dp0"
echo [R1206] Starting Intake Core Fix...

REM Python 3 launcher wie gewohnt:
py -3 -u "%~dp0Runner_1206_FixIntakeCore.py"
set rc=%ERRORLEVEL%
if %rc% neq 0 (
  echo [R1206] FAILED (rc=%rc%). Siehe ..\debug_output.txt
  exit /b %rc%
)
echo [R1206] Done. Launching GUI...
py -3 -u "%~dp0..\main_gui.py"
exit /b 0
