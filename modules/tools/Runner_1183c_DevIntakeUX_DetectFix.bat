@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0\.."
set "PY=py"
set "PYFLAGS=-3 -u"

echo [R1183c] Installing Dev-Intake UX + DetectFix...
"%PY%" %PYFLAGS% "tools\Runner_1183c_DevIntakeUX_DetectFix.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [R1183c] FAILED (rc=%RC%). See debug_output.txt
  exit /b %RC%
)

echo [R1183c] OK. Launching Main GUI...
if exist "tools\Start_MainGui.bat" (
  call "tools\Start_MainGui.bat"
) else (
  "%PY%" %PYFLAGS% "main_gui.py"
)
exit /b 0
