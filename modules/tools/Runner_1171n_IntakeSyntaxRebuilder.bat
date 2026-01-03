@echo off
setlocal
pushd "%~dp0\.."
echo [1171n] IntakeSyntaxRebuilder: starte Rebuild...
py -3 -u tools\Runner_1171n_IntakeSyntaxRebuilder.py
set rc=%ERRORLEVEL%
if %rc% neq 0 (
  echo [1171n] FEHLER (rc=%rc%) – siehe debug_output.txt
) else (
  echo [1171n] OK – Syntax wiederhergestellt.
)
popd
exit /b %rc%
