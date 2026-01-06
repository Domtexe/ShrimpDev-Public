@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_983_IntakeFix.py
py -3 -u tools\Runner_983_IntakeFix.py
echo [END ] RC=%errorlevel%
pause
