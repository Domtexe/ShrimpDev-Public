@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0\.."
set ROOT=%cd%

echo [1173f] IntakeTabSafeAdd: starte Patch...
set SRC=%ROOT%\main_gui.py
set BAK=%ROOT%\_Archiv\main_gui.py.%RANDOM%%RANDOM%.bak

if not exist "%ROOT%\_Archiv" mkdir "%ROOT%\_Archiv"
copy /y "%SRC%" "%BAK%" >nul 2>&1

python tools\Runner_1173f_IntakeTabSafeAdd.py || (
  echo [1173f] FEHLER -> Rollback...
  copy /y "%BAK%" "%SRC%" >nul
  exit /b 1
)

echo [1173f] Patch erfolgreich, Syntax OK.
exit /b 0
