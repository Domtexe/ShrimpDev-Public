@echo off
setlocal
cd /d D:\ShrimpDev

echo [1174r] IntakeTabRebind: starte Patch...

rem Python runner ausführen
py -3 -u "tools\Runner_1174r_IntakeTabRebind.py"
set RC=%ERRORLEVEL%

if %RC% NEQ 0 (
  echo [1174r] FEHLER: Python-Runner RC=%RC%. Stelle ggf. manuell aus _Archiv wieder her.
  exit /b %RC%
)

echo [1174r] Patch erfolgreich, Syntax OK.
exit /b 0
