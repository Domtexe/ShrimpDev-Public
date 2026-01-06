@echo off
cd /d "D:\ShrimpDev"
rem Beispiel:
rem   tools\Runner_942_NewModule.bat module_shcut_mapper "Video/Audio DeepScan" 0.1.0
set NAME=%1
set DESC=%2
set VER=%3
if "%NAME%"=="" (
  echo Usage: Runner_942_NewModule.bat module_name "Description" 0.1.0
  exit /b 64
)
if "%VER%"=="" set VER=0.1.0
echo [RUN ] py -3 -u tools\Runner_942_NewModule.py %NAME% "%DESC%" %VER%
py -3 -u tools\Runner_942_NewModule.py %NAME% "%DESC%" %VER%
echo [END ] RC=%errorlevel%
exit /b %errorlevel%
