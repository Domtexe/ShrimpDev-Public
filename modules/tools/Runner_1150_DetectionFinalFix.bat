@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1150] DetectionFinalFix
pushd "%~dp0\.." 1>nul 2>nul || ( echo [R1150] CD-Fehler & exit /b 2 )

rem Python-Launcher bevorzugen
set "PYCMD="
where py     >nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD ( where python >nul 2>nul && set "PYCMD=python -X utf8 -u" )
if not defined PYCMD ( echo [R1150] Fehler: Weder 'py' noch 'python' im PATH. & popd & exit /b 9009 )

%PYCMD% "tools\Runner_1150_DetectionFinalFix.py"
set "RC=%ERRORLEVEL%"

popd
echo [R1150] Ende (RC=%RC%)
exit /b %RC%
