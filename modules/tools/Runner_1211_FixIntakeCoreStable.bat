@echo off
setlocal
title [R1211] FixIntakeCoreStable
cd /d "%~dp0"
echo [R1211] FixIntakeCoreStable starting...
py -3 -u "%~dp0Runner_1211_FixIntakeCoreStable.py"
set rc=%errorlevel%
if %rc% neq 0 (
  echo [R1211] FAILED. Siehe ..\debug_output.txt
  exit /b %rc%
)
echo [R1211] DONE. Starte GUI...
py -3 -u ..\main_gui.py
exit /b 0
