@echo off
setlocal ENABLEDELAYEDEXPANSION
pushd "%~dp0\.."
echo [1171e] IntakeToolbarFix: starte sicheren Patch...
py -3 -u "tools\Runner_1171e_IntakeToolbarFix.py"
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1171e] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1171e] OK. Siehe debug_output.txt
)
popd
exit /B %rc%
