@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0\.."

echo [1173k] MainGuiCallRelocate: starte Patch...
set TARGET=main_gui.py
set ARCH=_Archiv
for /f "tokens=1-3 delims=/:. " %%a in ('echo %date% %time%') do set TS=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TS=%TS: =0%

if not exist "%ARCH%" mkdir "%ARCH%"
copy /y "%TARGET%" "%ARCH%\%TARGET%.%TS%.bak" >nul
if errorlevel 1 (
  echo [1173k] Backup FEHLER. Abbruch.
  exit /b 1
)

python tools\Runner_1173k_MainGuiCallRelocate.py
set rc=%ERRORLEVEL%
if %rc% NEQ 0 (
  echo [1173k] FEHLER. Stelle Backup wieder her...
  copy /y "%ARCH%\%TARGET%.%TS%.bak" "%TARGET%" >nul
  exit /b %rc%
)

echo [1173k] Patch erfolgreich, Syntax OK.
exit /b 0
