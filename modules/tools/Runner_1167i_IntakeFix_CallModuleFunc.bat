@echo off
setlocal
cd /d "%~dp0\.."
set PY=python
set TARGET=modules\module_code_intake.py
set TS=%DATE:~-4%%DATE:~3,2%%DATE:~0,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%
set TS=%TS: =0%
echo [1167i] Patch: Call module-level helper in _build_ui()...
copy "%TARGET%" "_Archiv\module_code_intake.py.%TS%.bak" >nul
%PY% tools\Runner_1167i_IntakeFix_CallModuleFunc.py || goto :err
echo [1167i] Syntax-Check OK. Fertig.
exit /b 0
:err
echo [1167i] FEHLER. Backup liegt unter _Archiv\module_code_intake.py.%TS%.bak
exit /b 1
