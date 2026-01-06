@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_970_AllInOneInstall.py
py -3 -u tools\Runner_970_AllInOneInstall.py
echo [END ] RC=%errorlevel%
pause
