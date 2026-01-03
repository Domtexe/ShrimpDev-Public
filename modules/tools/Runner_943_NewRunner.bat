@echo off
cd /d "D:\ShrimpDev"
rem Beispiel:
rem   tools\Runner_943_NewRunner.bat 950 "Beschreibung des Runners"
set ID=%1
set DESC=%2
if "%ID%"=="" (
  echo Usage: Runner_943_NewRunner.bat 950 "Beschreibung"
  exit /b 64
)
echo [RUN ] py -3 -u tools\Runner_943_NewRunner.py %ID% "%DESC%"
py -3 -u tools\Runner_943_NewRunner.py %ID% "%DESC%"
echo [END ] RC=%errorlevel%
exit /b %errorlevel%