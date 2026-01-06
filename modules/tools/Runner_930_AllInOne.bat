@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_930_AllInOne.py
py -3 -u tools\Runner_930_AllInOne.py
echo [END ] RC=%errorlevel%
pause
