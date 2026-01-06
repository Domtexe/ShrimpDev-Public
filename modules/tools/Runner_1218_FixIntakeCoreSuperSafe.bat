@echo off
setlocal
pushd %~dp0
echo [R1218] FixIntakeCoreSuperSafe starting...
py -3 -u Runner_1218_FixIntakeCoreSuperSafe.py
set rc=%ERRORLEVEL%
echo [R1218] Done. rc=%rc%
popd
exit /b %rc%
