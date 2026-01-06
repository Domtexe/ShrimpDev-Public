@echo off
setlocal
echo [1175c] SmokeMainOnly: starte Syntax/Future-Check...
where py >nul 2>&1 && (set PY=py -3) || (set PY=python)
%PY% - <<PYCODE
from __future__ import annotations
import sys, ast
p = r"D:\ShrimpDev\main_gui.py"
try:
    with open(p,"r",encoding="utf-8") as f: src=f.read()
    ast.parse(src)
    print("[1175c] Syntax OK.")
except SyntaxError as e:
    print(f"[1175c] SyntaxError: line {e.lineno}: {e.msg}")
    sys.exit(1)
PYCODE
if errorlevel 1 (echo [1175c] FEHLER. & exit /b 1)
echo [1175c] OK.
endlocal
