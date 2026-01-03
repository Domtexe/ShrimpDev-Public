@echo off
setlocal
cd /d D:\ShrimpDev
echo [1174s] MainGuiSmoke: starte Check...
py -3 -u "tools\Runner_1174s_MainGuiSmoke.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [1174s] FEHLER RC=%RC%. Siehe debug_output.txt
  exit /b %RC%
)
echo [1174s] OK.
exit /b 0
