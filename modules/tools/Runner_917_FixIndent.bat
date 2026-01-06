@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_917_FixIndent.py
py -3 -u tools\Runner_917_FixIndent.py
echo [END ] RC=%errorlevel%
pause
