@echo off
setlocal enableextensions
title [1176d] IntakeShimHotfix

cd /d D:\ShrimpDev
echo [1176d] Starte Patch...

rem --- Backups ---
if not exist _Archiv mkdir _Archiv
copy /y main_gui.py _Archiv\main_gui.py.%DATE:~-4%%DATE:~3,2%%DATE:~0,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%.bak >nul
copy /y modules\module_shim_intake.py _Archiv\module_shim_intake.py.%DATE:~-4%%DATE:~3,2%%DATE:~0,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%.bak >nul
copy /y modules\module_gate_smoke.py _Archiv\module_gate_smoke.py.%DATE:~-4%%DATE:~3,2%%DATE:~0,2%_%TIME:~0,2%%TIME:~3,2%%TIME:~6,2%.bak >nul 2>nul

rem --- Python-Patcher ---
py -3 -u tools\Runner_1176d_IntakeShimHotfix.py
if errorlevel 1 (
  echo [1176d] FEHLER beim Patch. Siehe debug_output.txt
  exit /b 1
)

rem --- Smoke-Test: nur Syntax ---
py -3 - <<PY
import py_compile, sys
try:
    py_compile.compile("main_gui.py", doraise=True)
    py_compile.compile("modules\\module_shim_intake.py", doraise=True)
    py_compile.compile("modules\\module_code_intake.py", doraise=True)
    print("[1176d] Syntax OK.")
    sys.exit(0)
except Exception as e:
    print("[1176d] SyntaxCheck FEHLER:", e)
    sys.exit(2)
PY
if errorlevel 1 exit /b 2

echo [1176d] Patch erfolgreich, Syntax OK.
echo [1176d] Du kannst jetzt "py -3 main_gui.py" starten.
exit /b 0
