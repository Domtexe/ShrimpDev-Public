@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_940_CoreKit.py
py -3 -u tools\Runner_940_CoreKit.py
echo [END ] RC=%errorlevel%
pause
