@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0\.."
echo [1170b] IntakeBindRepair: safe & idempotent Patch starten...
py -3 -u "tools\Runner_1170b_IntakeBindRepair.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1170b] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1170b] OK. Siehe debug_output.txt
)
popd
exit /B %rc%
