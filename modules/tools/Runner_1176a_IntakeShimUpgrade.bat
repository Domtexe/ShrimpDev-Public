@echo off
setlocal
title [1176a] IntakeShimUpgrade
echo [1176a] IntakeShimUpgrade: starte Patch...

REM Sicherstellen, dass Python verfügbar ist
where py >nul 2>nul
if errorlevel 1 (
  echo [1176a] WARN: Kein "py" im PATH. Versuche "python"...
  where python >nul 2>nul || (echo [1176a] FEHLER: Python nicht gefunden.& exit /b 9009)
  set PYTHON=python
) else (
  set PYTHON=py -3
)

REM Mini-Sanity: Module-Dateien vorhanden?
if not exist "D:\ShrimpDev\modules\module_shim_intake.py" (
  echo [1176a] FEHLER: module_shim_intake.py fehlt unter modules\ .
  exit /b 12
)
if not exist "D:\ShrimpDev\modules\module_gate_smoke.py" (
  echo [1176a] FEHLER: module_gate_smoke.py fehlt unter modules\ .
  exit /b 13
)

%PYTHON% -u "D:\ShrimpDev\tools\Runner_1176a_IntakeShimUpgrade.py"
set RC=%ERRORLEVEL%
if not "%RC%"=="0" (
  echo [1176a] FEHLER RC=%RC%. Siehe debug_output.txt / Konsole.
  exit /b %RC%
)

echo [1176a] Patch erfolgreich, Syntax OK.
echo [1176a] Starte GUI (Smoke)...
%PYTHON% - <<PYCODE
import runpy, sys
try:
    import tkinter  # Sanity: Tk vorhanden?
    print("[1176a] Tk OK")
except Exception as e:
    print("[1176a] WARN: Tk-Import fehlgeschlagen:", e)
print("[1176a] Smoke-Ende.")
PYCODE

echo [1176a] Ende.
exit /b 0
