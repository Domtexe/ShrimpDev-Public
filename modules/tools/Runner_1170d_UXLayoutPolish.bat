@echo off
setlocal
pushd "%~dp0\.."
echo [1170d] Patch: UX Layout Polish...
py -3 -u "tools\Runner_1170d_UXLayoutPolish.py"
set rc=%ERRORLEVEL%
if %rc% neq 0 (echo [1170d] FEHLER. Siehe debug_output.txt) else (echo [1170d] OK.)
popd
exit /b %rc%
