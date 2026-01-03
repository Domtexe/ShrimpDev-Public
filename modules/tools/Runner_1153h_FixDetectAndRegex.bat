@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1153h] FixDetectAndRegex
set "CWD=%~dp0..\"
pushd "%CWD%" || ( echo [R1153h] CD-Fehler & exit /b 2 )

rem Python-Launcher bevorzugen
where py 1>nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD ( where python 1>nul 2>nul && set "PYCMD=python -X utf8 -u" )
if not defined PYCMD ( echo [R1153h] Fehler: Weder 'py' noch 'python' im PATH. & popd & exit /b 9009 )

set "SCRIPT=tools\Runner_1153h_FixDetectAndRegex.py"
echo [R1153h] Script: %SCRIPT%
%PYCMD% "%SCRIPT%"
set RC=%ERRORLEVEL%
echo [R1153h] Ende (RC=%RC%)
popd
exit /b %RC%
