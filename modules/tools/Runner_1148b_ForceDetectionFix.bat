@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1148b] ForceDetectionFix
pushd "%~dp0\.." 1>nul 2>nul || ( echo [R1148b] CD-Fehler & exit /b 2 )

set "PYCMD="
where py     >nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD ( where python >nul 2>nul && set "PYCMD=python -X utf8 -u" )
if not defined PYCMD ( echo [R1148b] Fehler: Weder 'py' noch 'python' im PATH. & popd & exit /b 9009 )

%PYCMD% "tools\Runner_1148b_ForceDetectionFix.py"
set "RC=%ERRORLEVEL%"
popd
echo [R1148b] Ende (RC=%RC%)
exit /b %RC%
