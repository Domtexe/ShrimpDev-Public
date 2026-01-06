@echo off
setlocal
cd /d "%~dp0\.."
set "ROOT=%CD%"
set "PY=py"
set "PYFLAGS=-3 -u"

echo [R1181b] Starting MainGuiIndentFix...
"%PY%" %PYFLAGS% "tools\Runner_1181b_MainGuiIndentFix.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [R1181b] FAILED (rc=%RC%). Siehe debug_output.txt
  exit /b %RC%
)
echo [R1181b] OK. Launching GUI...
call "tools\Start_MainGui.bat"
exit /b 0
