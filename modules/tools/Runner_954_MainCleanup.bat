@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_954_MainCleanup.py
py -3 -u tools\Runner_954_MainCleanup.py
echo [END ] RC=%errorlevel%
pause
