@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1153] SmartDetect_AutoSave
pushd "%~dp0\.." 1>nul 2>nul || ( echo [R1153] CD-Fehler & exit /b 2 )

set "PYCMD="
where py     >nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD ( where python >nul 2>nul && set "PYCMD=python -X utf8 -u" )
if not defined PYCMD ( echo [R1153] Fehler: Weder 'py' noch 'python' im PATH. & popd & exit /b 9009 )

%PYCMD% "tools\Runner_1153_SmartDetect_AutoSave.py"
set "RC=%ERRORLEVEL%"

popd
echo [R1153] Ende (RC=%RC%)
exit /b %RC%
