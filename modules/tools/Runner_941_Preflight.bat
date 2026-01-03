@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_941_Preflight.py
py -3 -u tools\Runner_941_Preflight.py
echo [END ] RC=%errorlevel%
exit /b %errorlevel%
