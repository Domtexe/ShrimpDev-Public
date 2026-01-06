@echo off

cd /d "D:\ShrimpDev"

set PY=py -3

echo [START] ShrimpDev visible (%date% %time%)>> debug_output.txt

%PY% -u main_gui.py 1>> debug_output.txt 2>>&1

