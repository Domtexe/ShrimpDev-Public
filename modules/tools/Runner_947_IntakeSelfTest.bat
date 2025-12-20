@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_947_IntakeSelfTest.py
py -3 -u tools\Runner_947_IntakeSelfTest.py
echo [END ] RC=%errorlevel%
pause
