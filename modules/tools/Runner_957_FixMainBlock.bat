@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_957_FixMainBlock.py
py -3 -u tools\Runner_957_FixMainBlock.py
echo [END ] RC=%errorlevel%
pause
