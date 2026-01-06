@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0\.."
echo [1167b] Prüfe GUI-Intake-Mount...
py -3 -u "tools\Runner_1167b_GUIIntakePresenceCheck.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1167b] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1167b] OK. Siehe debug_output.txt
)
popd
exit /B %rc%
