@echo off
setlocal
pushd "%~dp0\.."
echo [1173c] IntakeTTKImportFix: starte Patch...
py -3 -u "tools\Runner_1173c_IntakeTTKImportFix.py"
set rc=%ERRORLEVEL%
if %rc% neq 0 (
  echo [1173c] FEHLER (rc=%rc%). Siehe debug_output.txt
) else (
  echo [1173c] OK. Syntax-Check bestanden.
)
popd
exit /b %rc%
