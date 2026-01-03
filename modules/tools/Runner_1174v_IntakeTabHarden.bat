@echo off
setlocal
cd /d D:\ShrimpDev
echo [1174v] IntakeTabHarden: starte Patch...
py -3 -u tools\Runner_1174v_IntakeTabHarden.py
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [1174v] FEHLER RC=%RC%. Rollback wurde ggf. bereits ausgefuehrt. Siehe debug_output.txt
  exit /b %RC%
)
echo [1174v] Patch uebernommen, Syntax OK.
exit /b 0
