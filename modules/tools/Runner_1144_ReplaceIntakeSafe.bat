@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1144] ReplaceIntakeSafe
pushd "%~dp0\.."  || ( echo [R1144] CD-Fehler & exit /b 2 )

set "PYCMD="
where py     >nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD ( where python >nul 2>nul && set "PYCMD=python -X utf8 -u" )
if not defined PYCMD ( echo [R1144] Fehler: Weder 'py' noch 'python' im PATH. & popd & exit /b 9009 )

%PYCMD% "tools\Runner_1144_ReplaceIntakeSafe.py"
set "RC=%ERRORLEVEL%"

popd
echo [R1144] Ende (RC=%RC%)
exit /b %RC%
