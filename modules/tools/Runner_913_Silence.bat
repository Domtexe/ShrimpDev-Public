@echo off
cd /d "D:\ShrimpDev"
rem Popups/Reports nur bei Fehlern (Default). Falls gewünscht:
rem set SHRIMPDEV_POPUPS=errors
rem set SHRIMPDEV_REPORTS=errors
py -3 -u tools\Runner_913_Silence.py
set RC=%ERRORLEVEL%
echo [R913] RC=%RC%
exit /b %RC%
