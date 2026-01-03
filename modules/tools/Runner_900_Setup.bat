@echo off
setlocal
cd /d "D:\ShrimpDev"
REM --- Python-Runner ausführen (still, ohne Fensterflackern)
where py >nul 2>nul || (echo [R900] Python nicht gefunden.& exit /b 1)
echo [RUN ] py -3 -u tools\Runner_900_Setup.py
py -3 -u tools\Runner_900_Setup.py
set RC=%ERRORLEVEL%
echo [END ] RC=%RC%
pause >nul
exit /b %RC%
