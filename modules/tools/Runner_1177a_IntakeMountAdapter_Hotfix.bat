@echo off
cd /d "%~dp0\.."
echo [1177a-Hotfix] Repairing _e name error...
py -3 -u "tools\Runner_1177a_IntakeMountAdapter_Hotfix.py"
echo Fertig.
pause
