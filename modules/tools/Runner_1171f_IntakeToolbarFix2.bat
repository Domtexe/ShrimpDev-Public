@echo off
setlocal
pushd "%~dp0\.."
echo [1171f] IntakeToolbarFix2: starte sicheren Patch...
py -3 -u "tools\Runner_1171f_IntakeToolbarFix2.py"
set rc=%ERRORLEVEL%
if %rc% neq 0 (
  echo [1171f] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1171f] OK. Siehe debug_output.txt
)
popd
exit /b %rc%
