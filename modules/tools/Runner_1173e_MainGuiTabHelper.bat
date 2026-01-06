@echo off
setlocal
cd /d "%~dp0"
python Runner_1173e_MainGuiTabHelper.py || goto :e
echo [1173e] OK.
exit /b 0
:e
echo [1173e] FEHLER.
exit /b 1
