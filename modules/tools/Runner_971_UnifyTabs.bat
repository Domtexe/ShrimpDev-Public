@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_971_UnifyTabs.py
py -3 -u tools\Runner_971_UnifyTabs.py
echo [END ] RC=%errorlevel%
pause
