@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0\.."
echo [1171a] IntakeUX&Detect: sicherer Patch startet...
py -3 -u "tools\Runner_1171a_IntakeUXAndDetect.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1171a] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1171a] OK. Siehe debug_output.txt
)
popd
exit /B %rc%
