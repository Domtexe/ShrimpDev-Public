@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1153g] SafeRegexAllIntake
pushd "%~dp0\.." 1>nul 2>nul || ( echo [R1153g] CD-Fehler & exit /b 2 )

set "PYCMD="
where py     >nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD ( where python >nul 2>nul && set "PYCMD=python -X utf8 -u" )
if not defined PYCMD ( echo [R1153g] Fehler: Weder 'py' noch 'python' im PATH. & popd & exit /b 9009 )

%PYCMD% "tools\Runner_1153g_SafeRegexAllIntake.py"
set "RC=%ERRORLEVEL%"

popd
echo [R1153g] Ende (RC=%RC%)
exit /b %RC%
