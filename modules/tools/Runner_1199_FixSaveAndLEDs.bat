@echo off
setlocal
echo [R1199] Starting FixSaveAndLEDs...

REM Defensive: python launcher
set PY=py -3 -u

REM Run patcher
%PY% "%~dp0Runner_1199_FixSaveAndLEDs.py" || goto :fail

REM Relaunch Main GUI
call "%~dp0Start_MainGui.bat"
echo [R1199] Done.
exit /b 0

:fail
echo [R1199] FAILED. See _Archiv\debug_output.txt (if any).
exit /b 1
