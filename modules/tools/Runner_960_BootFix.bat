@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_960_BootFix.py
py -3 -u tools\Runner_960_BootFix.py
echo [END ] RC=%errorlevel%
pause
