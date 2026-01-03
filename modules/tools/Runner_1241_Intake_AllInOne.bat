@echo off
setlocal
cd /d "%~dp0"
echo [R1241] Intake_AllInOne starting...
py -3 -u "%~dp0Runner_1241_Intake_AllInOne.py"
set rc=%errorlevel%
echo [R1241] Done. rc=%rc%
exit /b %rc%
