@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_961_MenuFix.py
py -3 -u tools\Runner_961_MenuFix.py
echo [END ] RC=%errorlevel%
pause
