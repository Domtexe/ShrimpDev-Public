@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_910_Install.py
py -3 -u tools\Runner_910_Install.py
echo [END ] RC=%errorlevel%
pause
