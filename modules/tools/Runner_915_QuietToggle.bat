@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_915_QuietToggle.py
py -3 -u tools\Runner_915_QuietToggle.py
echo [END ] RC=%errorlevel%
pause
