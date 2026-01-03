@echo off
setlocal
cd /d "%~dp0\.."
echo [R1213] FixIntakeCoreStable starting...
py -3 -u tools\Runner_1213_FixIntakeCoreStable.py || goto :err
echo [R1213] Done. Launching GUI...
py -3 -u main_gui.py
goto :eof
:err
echo [R1213] FAILED. See debug_output.txt
exit /b 1
