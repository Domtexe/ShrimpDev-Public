@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_918_FixIndentMain.py
py -3 -u tools\Runner_918_FixIndentMain.py
echo [END ] RC=%errorlevel%
pause
