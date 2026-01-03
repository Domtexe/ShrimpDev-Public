@echo off
setlocal ENABLEDELAYEDEXPANSION
title [R1216] FixIntakeCore Final

set ROOT=%~dp0..
set MOD=%ROOT%\modules\module_code_intake.py
set ARCH=%ROOT%\_Archiv
for /f %%a in ('powershell -NoP -C "(Get-Date).ToString('yyyyMMdd_HHmmss')"') do set TS=%%a

echo [R1216] FixIntakeCore starting...
if not exist "%MOD%" (
  echo [R1216] ERROR: %MOD% nicht gefunden.
  exit /b 1
)

if not exist "%ARCH%" mkdir "%ARCH%"
copy "%MOD%" "%ARCH%\module_code_intake.py.%TS%.bak" >nul
echo [R1216] Backup: %ARCH%\module_code_intake.py.%TS%.bak

py -3 -u "%~dp0Runner_1216_FixIntakeCore_Final.py"
if errorlevel 1 (
  echo [R1216] FAILED. Siehe debug_output.txt
  exit /b 1
)

echo [R1216] OK. Launching GUI...
py -3 -u "%ROOT%\main_gui.py"
exit /b 0
