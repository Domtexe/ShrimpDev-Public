@echo off
setlocal
pushd "%~dp0\.."
echo [1172] IntakeTabGuard: starte Patch...
py -3 -u tools\Runner_1172_IntakeTabGuard.py
set rc=%ERRORLEVEL%
if %rc% neq 0 (
  echo [1172] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1172] OK. Syntax-Check bestanden.
)
popd
exit /b %rc%
