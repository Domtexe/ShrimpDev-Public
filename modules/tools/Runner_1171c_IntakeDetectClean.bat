@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0\.."
echo [1171c] IntakeDetect+Clean: sicherer Patch startet...
py -3 -u "tools\Runner_1171c_IntakeDetectClean.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1171c] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1171c] OK. Siehe debug_output.txt
)
popd
exit /B %rc%
