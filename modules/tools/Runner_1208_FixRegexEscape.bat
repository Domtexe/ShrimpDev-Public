@echo off
setlocal
echo [R1208] FixRegexEscape running...
py -3 -u "%~dp0Runner_1208_FixRegexEscape.py"
echo [R1208] Done. Danach Runner_1207_FixIntakeCoreSafe.bat erneut starten.
endlocal
