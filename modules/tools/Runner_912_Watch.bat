@echo off
cd /d "D:\ShrimpDev"
powershell -NoP -W Hidden -C "Start-Process -WindowStyle Hidden 'py' -ArgumentList '-3','-u','D:\ShrimpDev\tools\Runner_912_Watch.py'"
echo [R912] Watch gestartet (hidden)
pause
