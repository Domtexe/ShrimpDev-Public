@echo off
setlocal
pushd "%~dp0\.."
echo [1171q] IntakeCleanAndExternalize: starte...
py -3 -u tools\Runner_1171q_IntakeCleanAndExternalize.py
set rc=%ERRORLEVEL%
if %rc% neq 0 (
  echo [1171q] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1171q] OK. Syntax-Check bestanden.
)
popd
exit /b %rc%
