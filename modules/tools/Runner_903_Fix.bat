@echo off
cd /d "D:\ShrimpDev"
py -3 -u tools\Runner_903_Fix.py
echo [END ] RC=%errorlevel%
pause
