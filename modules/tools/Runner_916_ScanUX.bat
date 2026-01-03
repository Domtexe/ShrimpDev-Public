@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_916_ScanUX.py
py -3 -u tools\Runner_916_ScanUX.py
echo [END ] RC=%errorlevel%
pause
