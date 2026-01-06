@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_953_FixLoneTry.py
py -3 -u tools\Runner_953_FixLoneTry.py
echo [END ] RC=%errorlevel%
pause
