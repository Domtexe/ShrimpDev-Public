@echo off
setlocal
pushd "%~dp0\.."
echo [1171j] IntakeToolbarReflowTopLevel: starte sicheren Patch...
py -3 -u "tools\Runner_1171j_IntakeToolbarReflowTopLevel.py"
set rc=%ERRORLEVEL%
if %rc% neq 0 (
  echo [1171j] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1171j] OK. Siehe debug_output.txt
)
popd
exit /b %rc%
