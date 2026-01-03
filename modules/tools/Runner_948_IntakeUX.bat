@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_948_IntakeUX.py
py -3 -u tools\Runner_948_IntakeUX.py
echo [END ] RC=%errorlevel%
pause
