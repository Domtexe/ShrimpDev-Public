@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
cd ..

set "PY=py"
set "PYFLAGS=-3 -u"

echo [1180] Installing safe starters...
py -3 -u "tools\Runner_1180_StartFix.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [1180] FAILED (rc=%RC%). Siehe debug_output.txt
  exit /b %RC%
)

echo [1180] OK. Launching Main GUI...
call "tools\Start_MainGui.bat"
exit /b 0
