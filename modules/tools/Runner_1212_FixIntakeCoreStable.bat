@echo off
setlocal
pushd %~dp0\..
echo [R1212] FixIntakeCoreStable starting...
py -3 -u tools\Runner_1212_FixIntakeCoreStable.py
set rc=%ERRORLEVEL%
echo [R1212] Done. rc=%rc%
popd
exit /b %rc%
