@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_991_AllTabsIntegrate.py
py -3 -u tools\Runner_991_AllTabsIntegrate.py
echo [END ] RC=%errorlevel%
pause
