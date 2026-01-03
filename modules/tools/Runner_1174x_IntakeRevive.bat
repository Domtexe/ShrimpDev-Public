@echo off
setlocal enabledelayedexpansion
title [1174x] IntakeRevive: Restore + Guards

set ROOT=D:\ShrimpDev
set TOOLS=%ROOT%\tools
set ARCH=%ROOT%\_Archiv
set MODS=%ROOT%\modules
set TARGET=%MODS%\module_code_intake.py
set MAIN=%ROOT%\main_gui.py
set PY=py -3 -u

echo [1174x] IntakeRevive: starte...
if not exist "%ARCH%" (
  echo [1174x] FEHLER: Archiv-Ordner fehlt: "%ARCH%"
  goto :eof
)

:: Backup aktueller Dateien
for %%F in ("%TARGET%" "%MAIN%") do (
  if exist "%%~F" (
    set TS=%DATE:~6,4%%DATE:~3,2%%DATE:~0,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
    set TS=!TS: =0!
    copy /y "%%~F" "%ARCH%\%%~nxF.!TS!.bak" >nul
  )
)

echo [1174x] Finde kompilierfähiges Intake-Backup...
%PY% "%TOOLS%\Runner_1174x_IntakeRevive.py" --restore-best-from-arch "%ARCH%" --target "%TARGET%" --main "%MAIN%"
set RC=%ERRORLEVEL%
if not "%RC%"=="0" (
  echo [1174x] FEHLER RC=%RC%. Abbruch. Siehe debug_output.txt
  goto :eof
)

echo [1174x] Smoke: starte GUI (nur Test)...
%PY% "%ROOT%\main_gui.py"
echo [1174x] Ende.
endlocal
