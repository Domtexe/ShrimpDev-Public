@echo off
setlocal ENABLEDELAYEDEXPANSION
title [1175h] IntakeCleanRestore

echo [1175h] IntakeCleanRestore: starte Patch...
cd /d D:\ShrimpDev

rem -- Sichere Ziel
set MOD=modules\module_code_intake.py
if not exist modules\ (echo [1175h] FEHLER: modules\-Ordner fehlt.& exit /b 2)

for /f "tokens=1-4 delims=.:/ " %%a in ("%date% %time%") do set TS=%%d%%c%%b_%%e%%f%%g
set BAK=_Archiv\module_code_intake.py.%TS%.bak
if not exist _Archiv\ mkdir _Archiv
copy /y "%MOD%" "%BAK%" >nul 2>&1

rem -- Starte Python-Runner
py -3 -u "tools\Runner_1175h_IntakeCleanRestore.py"
set RC=%ERRORLEVEL%

if %RC% NEQ 0 (
  echo [1175h] FEHLER RC=%RC%. Stelle ggf. Backup wieder her: %BAK%
  exit /b %RC%
)

echo [1175h] OK. Ende.
exit /b 0
