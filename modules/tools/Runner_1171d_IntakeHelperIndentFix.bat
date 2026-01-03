@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0\.."
echo [1171d] IntakeHelperIndentFix: starte Reparatur...
py -3 -u "tools\Runner_1171d_IntakeHelperIndentFix.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1171d] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1171d] OK. Siehe debug_output.txt
)
popd
exit /B %rc%
