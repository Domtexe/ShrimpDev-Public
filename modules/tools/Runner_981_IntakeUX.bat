@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_981_IntakeUX.py
py -3 -u tools\Runner_981_IntakeUX.py
echo [END ] RC=%errorlevel%
pause
