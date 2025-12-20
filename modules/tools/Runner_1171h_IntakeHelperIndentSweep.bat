@echo off
setlocal
pushd "%~dp0\.."
echo [1171h] IntakeHelperIndentSweep: starte Reparatur...
py -3 -u "tools\Runner_1171h_IntakeHelperIndentSweep.py"
set rc=%ERRORLEVEL%
if %rc% neq 0 (
  echo [1171h] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1171h] OK. Siehe debug_output.txt
)
popd
exit /b %rc%
