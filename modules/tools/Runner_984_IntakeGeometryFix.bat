@echo off
cd /d "D:\ShrimpDev"
echo [RUN ] py -3 -u tools\Runner_984_IntakeGeometryFix.py
py -3 -u tools\Runner_984_IntakeGeometryFix.py
echo [END ] RC=%errorlevel%
pause
