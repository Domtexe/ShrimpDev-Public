@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1154d] FixIntakeToolbarAndGuard
pushd "%~dp0\.." 1>nul 2>nul || ( echo [R1154d] CD-Fehler & exit /b 2 )

set "PYCMD="
where py     >nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD ( where python >nul 2>nul && set "PYCMD=python -X utf8 -u" )
if not defined PYCMD ( echo [R1154d] Fehler: Weder 'py' noch 'python' im PATH. & popd & exit /b 9009 )

%PYCMD% "tools\Runner_1154d_FixIntakeToolbarAndGuard.py"
set "RC=%ERRORLEVEL%"

popd
echo [R1154d] Ende (RC=%RC%)
exit /b %RC%
