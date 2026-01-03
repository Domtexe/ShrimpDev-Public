@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_946_IntakeSmart.py
py -3 -u tools\Runner_946_IntakeSmart.py
echo [END ] RC=%errorlevel%
pause
