@echo off
setlocal
cd /d "%~dp0\.."
echo [R1132] FixIntakeActions
REM Python 3 bevorzugt, fällt auf "py" zurück
where py >nul 2>&1 && (set "PY=py -3") || (set "PY=py")
%PY% -u "tools\Runner_1132_FixIntakeActions.py"
set RC=%ERRORLEVEL%
echo [R1132] Ende (RC=%RC%)
exit /b %RC%
