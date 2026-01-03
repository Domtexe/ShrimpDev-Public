@echo off
setlocal ENABLEDELAYEDEXPANSION
title [R1242] Intake Repair + Integrate (All-in-One)

set PY=py -3 -u
set ROOT=%~dp0\..
set MOD=%ROOT%\modules
set ARCH=%ROOT%\_Archiv

echo [R1242] Starting...

rem -- 1) Safety-Backup
for /f "tokens=1-4 delims=/ " %%a in ('date /t') do set DATE=%%d%%b%%c
for /f "tokens=1-2 delims=: " %%a in ('time /t') do set TIME=%%a%%b
set TS=%DATE%_%TIME%
set TS=%TS:/=%& set TS=%TS::=%

if not exist "%ARCH%" mkdir "%ARCH%"
if exist "%MOD%\module_code_intake.py" copy /Y "%MOD%\module_code_intake.py" "%ARCH%\module_code_intake.py.%TS%.bak" >nul

rem -- 2) Run Python fixer (recovery + patch + integration)
"%PY%" "%ROOT%\tools\Runner_1242_Intake_RepairAndIntegrate.py"
set RC=%ERRORLEVEL%
if not "%RC%"=="0" (
  echo [R1242] Python fixer failed. rc=%RC%
  echo [R1242] FAILED. See debug_output.txt
  exit /b %RC%
)

echo [R1242] Done. rc=0
echo [Start] Using: "%PY%"  ..\main_gui.py
"%PY%" "%ROOT%\main_gui.py"
exit /b 0
