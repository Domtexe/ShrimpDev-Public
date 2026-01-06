@echo off
setlocal
cd /d "D:\ShrimpDev"
set SHRIMPDEV_PORT=9488
cscript //nologo tools\start_quiet.vbs  //B
rem start_quiet.vbs startet main_gui; wir starten unser Tail separat, still:
powershell -NoP -W Hidden -C "Start-Process -WindowStyle Hidden 'py' -ArgumentList '-3','-u','D:\ShrimpDev\tools\Runner_902_LogTail.py'"
echo [R902] LogTail gestartet (hidden).
