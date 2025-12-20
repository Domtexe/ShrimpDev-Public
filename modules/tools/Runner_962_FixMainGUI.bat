@echo off
cd /d "D:\ShrimpDev"
py -3 -u tools\Runner_962_FixMainGUI.py
echo [END ] RC=%errorlevel%
pause
