@echo off
setlocal
echo [R1191] Installing Dev-Intake Clean...

set MOD=D:\ShrimpDev\modules\module_code_intake.py
set ARC=D:\ShrimpDev\_Archiv
if not exist "%ARC%" mkdir "%ARC%"
copy /y "%MOD%" "%ARC%\module_code_intake.py.%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%.bak" >nul 2>&1

py -3 -u "%~dp0Runner_1191_DevIntake_CleanInstall.py"
if errorlevel 1 goto :fail

call "%~dp0Start_MainGui.bat"
exit /b 0

:fail
echo [R1191] FAILED.
exit /b 1
