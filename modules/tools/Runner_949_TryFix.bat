@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_949_TryFix.py
py -3 -u tools\Runner_949_TryFix.py
echo [END ] RC=%errorlevel%
pause
