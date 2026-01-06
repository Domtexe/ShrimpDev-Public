@echo off
setlocal
echo [R1200] Starting DevIntake AutoDetect + UX polish...

rem Python 3 Launcher verwenden
py -3 -u "%~dp0Runner_1200_DevIntake_AutoDetectAndPolish.py"
if errorlevel 1 (
  echo [R1200] FAILED. See ..\debug_output.txt
  exit /b 1
)

echo [R1200] OK. Launching Main GUI...
call "%~dp0Start_MainGui.bat"
endlocal
