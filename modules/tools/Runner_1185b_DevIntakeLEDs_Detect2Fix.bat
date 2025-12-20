@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d "%~dp0"
set "PY=py"
set "PYFLAGS=-3 -u"

echo [R1185b] Patching triple-quote regex...
"%PY%" %PYFLAGS% "Runner_1185b_DevIntakeLEDs_Detect2Fix.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [R1185b] FAILED. Siehe debug_output.txt
  exit /b %RC%
)
echo [R1185b] OK. Starte erneut:
cd ..
call "tools\Start_MainGui.bat"
