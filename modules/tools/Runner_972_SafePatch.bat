@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_972_SafePatch.py
py -3 -u tools\Runner_972_SafePatch.py
echo [END ] RC=%errorlevel%
pause
