@echo off
setlocal
rem [R1204] FixIndent + AutoDetect + SaveAs mapping

set ROOT=D:\ShrimpDev
set PY=py -3 -u
set MOD=%ROOT%\modules\module_code_intake.py
set ARCH=%ROOT%\_Archiv
if not exist "%ARCH%" mkdir "%ARCH%"

echo [R1204] Starting FixIndent_AutoDetect_SaveAs...
copy /Y "%MOD%" "%ARCH%\module_code_intake.py.%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%.bak" >nul

"%PY%" "%~dp0Runner_1204_FixIndent_AutoDetect_SaveAs.py"
if errorlevel 1 (
  echo [R1204] FAILED. See ..\debug_output.txt
  exit /b 1
)

echo [R1204] OK. Launching Main GUI...
call "%ROOT%\tools\Start_MainGui.bat"
exit /b 0
