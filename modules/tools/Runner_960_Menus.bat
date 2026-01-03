@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_960_Menus.py
py -3 -u tools\Runner_960_Menus.py
echo [END ] RC=%errorlevel%
pause
