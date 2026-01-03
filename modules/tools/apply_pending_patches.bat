@echo off
setlocal
cd /d "D:\ShrimpDev"
set PENDING=_Pending
if not exist "%PENDING%" exit /b 0
for /r "%PENDING%" %%F in (*) do (
  set "REL=%%F"
  setlocal enabledelayedexpansion
  set "REL=!REL:D:\ShrimpDev\_Pending\=!"
  for %%# in ("!REL!") do (
    if not exist "D:\ShrimpDev\%%~dp#" mkdir "D:\ShrimpDev\%%~dp#"
    copy /y "%%F" "D:\ShrimpDev\!REL!" >nul
  )
  endlocal
)
for /f "delims=" %%D in ('dir /b /s /ad "%PENDING%" ^| sort /r') do rd "%%D" 2>nul
exit /b 0
