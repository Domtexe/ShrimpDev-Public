@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_935_FixMainGUI.py
py -3 -u tools\Runner_935_FixMainGUI.py
echo [END ] RC=%errorlevel%
pause
