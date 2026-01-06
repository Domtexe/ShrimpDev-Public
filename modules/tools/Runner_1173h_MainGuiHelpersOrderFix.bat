@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0\.."
set ROOT=%cd%
set SRC=%ROOT%\main_gui.py
set ARCH=%ROOT%\_Archiv

if not exist "%ARCH%" mkdir "%ARCH%"

set TS=%RANDOM%%RANDOM%
set BAK=%ARCH%\main_gui.py.%TS%.bak
copy /y "%SRC%" "%BAK%" >nul 2>&1

echo [1173h] MainGuiHelpersOrderFix: starte Patch...
python tools\Runner_1173h_MainGuiHelpersOrderFix.py || (
  echo [1173h] FEHLER -> Rollback auf %BAK%
  copy /y "%BAK%" "%SRC%" >nul
  exit /b 1
)
echo [1173h] OK. Backup: %BAK%
exit /b 0
