@echo off
setlocal
set R=Runner_1210_DevIntake_FixCoreAndUX
echo [%R%] Starting...

REM Python 3 launcher wie bei dir ueblich:
py -3 -u "%~dp0%~n0.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [%R%] FAILED (rc=%RC%). Siehe debug_output.txt
  exit /b %RC%
)
echo [%R%] Done.
exit /b 0
