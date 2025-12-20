@echo off
setlocal
echo [R1192] DevIntake UI Refine...
set TOOLS=%~dp0
set ROOT=%TOOLS%\..
set MOD=%ROOT%\modules\module_code_intake.py
set ARC=%ROOT%\_Archiv

if not exist "%ARC%" mkdir "%ARC%"
copy /y "%MOD%" "%ARC%\module_code_intake.py.%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%.bak" >nul 2>&1

py -3 -u "%~dp0Runner_1192_DevIntake_UIRefine.py"
if errorlevel 1 (
  echo [R1192] FAILED. Siehe debug_output.txt
  exit /b 1
)

call "%~dp0Start_MainGui.bat"
exit /b 0
