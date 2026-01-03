@echo off
setlocal ENABLEDELAYEDEXPANSION
echo [R1152] TableUX_Interactions
pushd "%~dp0\.." 1>nul 2>nul || ( echo [R1152] CD-Fehler & exit /b 2 )

set "PYCMD="
where py     >nul 2>nul && set "PYCMD=py -3 -X utf8 -u"
if not defined PYCMD ( where python >nul 2>nul && set "PYCMD=python -X utf8 -u" )
if not defined PYCMD ( echo [R1152] Fehler: Weder 'py' noch 'python' im PATH. & popd & exit /b 9009 )

%PYCMD% "tools\Runner_1152_TableUX_Interactions.py"
set "RC=%ERRORLEVEL%"

popd
echo [R1152] Ende (RC=%RC%)
exit /b %RC%
