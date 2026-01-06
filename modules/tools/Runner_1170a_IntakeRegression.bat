@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0\.."
echo [1170a] Intake-Regression (Verdrahtung) starten...
py -3 -u "tools\Runner_1170a_IntakeRegression.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1170a] CHECKS: FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1170a] CHECKS: OK. Siehe debug_output.txt
)
popd
exit /B %rc%
