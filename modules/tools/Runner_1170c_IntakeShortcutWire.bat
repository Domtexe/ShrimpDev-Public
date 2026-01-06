@echo off
setlocal
pushd "%~dp0\.."
echo [1170c] Patch: Keyboard-Shortcuts sicher verdrahten...
py -3 -u "tools\Runner_1170c_IntakeShortcutWire.py"
set rc=%ERRORLEVEL%
if %rc% neq 0 (echo [1170c] FEHLER. Siehe debug_output.txt) else (echo [1170c] OK.)
popd
exit /b %rc%
