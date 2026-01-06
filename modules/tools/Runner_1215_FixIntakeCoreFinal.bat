@echo off
setlocal
set ROOT=%~dp0..
set PY=py -3 -u

echo [R1215] FixIntakeCoreFinal starting...
%PY% "%ROOT%\tools\Runner_1215_FixIntakeCoreFinal.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [R1215] FAILED. See debug_output.txt
  exit /b %RC%
)

echo [R1215] OK. Launching GUI...
%PY% "%ROOT%\main_gui.py"
exit /b 0
