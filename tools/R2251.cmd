@echo off
setlocal

REM R2251 - Test Runner (stdout only)
python "%~dp0R2251.py"
exit /b %ERRORLEVEL%
