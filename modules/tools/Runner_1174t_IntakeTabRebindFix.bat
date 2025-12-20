@echo off
setlocal
cd /d D:\ShrimpDev
echo [1174t] IntakeTabRebindFix: starte Patch...
py -3 -u "tools\Runner_1174t_IntakeTabRebindFix.py"
set RC=%ERRORLEVEL%
if %RC% NEQ 0 (
  echo [1174t] FEHLER RC=%RC%. Rollback wurde ggf. bereits durchgefuehrt.
  exit /b %RC%
)
echo [1174t] Patch erfolgreich, Syntax OK.
exit /b 0
