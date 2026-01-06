@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_950.py
py -3 -u tools\Runner_950.py
echo [END ] RC=%errorlevel%
pause
