@echo off
setlocal
cd /d "%~dp0"
python Runner_1173d_IntakeFallbackReturnFix.py || goto :e
echo [1173d] OK.
exit /b 0
:e
echo [1173d] FEHLER.
exit /b 1
