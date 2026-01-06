@echo off
setlocal
echo [R1217] FixIntakeCoreSuperSafe starting...
py -3 -u "%~dp0Runner_1217_FixIntakeCoreSuperSafe.py" || goto :err
echo [R1217] Done. Launching GUI...
py -3 -u "%~dp0..\main_gui.py"
exit /b 0
:err
echo [R1217] FAILED. See console above.
exit /b 1
