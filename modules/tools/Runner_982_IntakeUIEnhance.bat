@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_982_IntakeUIEnhance.py
py -3 -u tools\Runner_982_IntakeUIEnhance.py
echo [END ] RC=%errorlevel%
pause
