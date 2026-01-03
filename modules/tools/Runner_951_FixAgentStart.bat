@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_951_FixAgentStart.py
py -3 -u tools\Runner_951_FixAgentStart.py
echo [END ] RC=%errorlevel%
pause
