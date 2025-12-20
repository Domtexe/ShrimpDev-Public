@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1142] DefuseSafe
pushd "%~dp0\.."  || ( echo [R1142] CD-Fehler & exit /b 2 )

set "PYCMD="
where py     >nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD ( where python >nul 2>nul && set "PYCMD=python -X utf8 -u" )
if not defined PYCMD ( echo [R1142] Fehler: Weder 'py' noch 'python' im PATH. & popd & exit /b 9009 )

%PYCMD% "tools\Runner_1142_DefuseSafe.py"
set "RC=%ERRORLEVEL%"

popd
echo [R1142] Ende (RC=%RC%)
exit /b %RC%
