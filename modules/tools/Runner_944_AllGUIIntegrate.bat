@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_944_AllGUIIntegrate.py
py -3 -u tools\Runner_944_AllGUIIntegrate.py
echo [END ] RC=%errorlevel%
pause
