@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_952_FixTryEverywhere.py
py -3 -u tools\Runner_952_FixTryEverywhere.py
echo [END ] RC=%errorlevel%
pause
