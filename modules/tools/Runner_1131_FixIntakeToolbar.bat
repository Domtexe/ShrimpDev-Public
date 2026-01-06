@echo off
setlocal
pushd "%~dp0\.." || ( echo [R1131] CD-Fehler & exit /b 2 )
echo [R1131] FixIntakeToolbar

where py >NUL 2>&1
if %ERRORLEVEL% EQU 0 (
  py -3 "tools\Runner_1131_FixIntakeToolbar.py"
) else (
  where python >NUL 2>&1 || ( echo [R1131] Python nicht gefunden & popd & exit /b 9009 )
  python "tools\Runner_1131_FixIntakeToolbar.py"
)

set RC=%ERRORLEVEL%
popd
echo [R1131] Ende (RC=%RC%)
exit /b %RC%
