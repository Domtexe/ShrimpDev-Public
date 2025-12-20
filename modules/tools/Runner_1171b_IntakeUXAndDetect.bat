@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0\.."
echo [1171b] IntakeUX&Detect (safe)...
py -3 -u "tools\Runner_1171b_IntakeUXAndDetect.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1171b] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1171b] OK. Siehe debug_output.txt
)
popd
exit /B %rc%
