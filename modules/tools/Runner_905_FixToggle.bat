@echo off
cd /d "D:\ShrimpDev"
py -3 -u tools\Runner_905_FixToggle.py
echo [END ] RC=%ERRORLEVEL%
pause
