@echo off
setlocal
cd /d D:\ShrimpDev
echo [1174w] MainSyntaxSmoke: starte Syntax-Check...
py -3 -u tools\Runner_1174w_MainSyntaxSmoke.py
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [1174w] FEHLER RC=%RC%. Siehe debug_output.txt
  exit /b %RC%
)
echo [1174w] OK (Syntax).
exit /b 0
