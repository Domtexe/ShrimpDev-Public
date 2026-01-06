@echo off
setlocal ENABLEDELAYEDEXPANSION
cd /d "%~dp0\.."
set PY=py -3 -u

echo [R1177m] Starting FixMainAndGate Runner...
%PY% "tools\Runner_1177m_FixMainAndGate.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [R1177m] FAILED with exit code %RC%.
  exit /b %RC%
)

echo [R1177m] OK. Launching Main GUI...
call "tools\Start_MainGui.bat"
exit /b 0
