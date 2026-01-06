@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_980_DevConsolidate.py
py -3 -u tools\Runner_980_DevConsolidate.py
echo [END ] RC=%errorlevel%
pause
