@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0\.."
echo [1167h] Dumppe _INTAKE_ERR aus main_gui...
py -3 -u "tools\Runner_1167h_IntakeErrDump.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1167h] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1167h] OK. Siehe _Reports\Intake_err.txt und debug_output.txt
)
popd
exit /B %rc%
