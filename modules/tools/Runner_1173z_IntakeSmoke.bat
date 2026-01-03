@echo off
setlocal
cd /d "%~dp0"
python Runner_1173z_IntakeSmoke.py || goto :e
echo [1173z] Smoke OK.
exit /b 0
:e
echo [1173z] Smoke FEHLER.
exit /b 1
