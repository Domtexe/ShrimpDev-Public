@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_904_WarnSilence.py
py -3 -u tools\Runner_904_WarnSilence.py
echo [END ] RC=%errorlevel%
pause
