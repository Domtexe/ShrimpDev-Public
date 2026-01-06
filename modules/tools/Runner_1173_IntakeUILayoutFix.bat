@echo off
setlocal
pushd "%~dp0\.."
echo [1173] IntakeUILayoutFix: starte Patch...
py -3 -u "tools\Runner_1173_IntakeUILayoutFix.py"
set rc=%ERRORLEVEL%
if %rc% neq 0 (
  echo [1173] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1173] OK. Syntax-Check bestanden.
)
popd
exit /b %rc%
