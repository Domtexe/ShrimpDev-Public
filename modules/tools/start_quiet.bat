@echo off
setlocal
cd /d "D:\ShrimpDev"
set "LOG=debug_output.txt"
if exist "%LOG%" for %%F in ("%LOG%") do if %%~zF gtr 2097152 (
  for /f "tokens=1-4 delims=/:. " %%a in ("%date% %time%") do set TS=%%d%%b%%a_%%c
  ren "%LOG%" "debug_output_%TS%.log"
)
cscript //nologo "tools\start_quiet.vbs"
echo [INFO ] ShrimpDev quiet gestartet – siehe debug_output.txt
endlocal
