# -*- coding: utf-8 -*-
"""
Minimaler Smoke-Gate (nicht-destruktiv).
"""
from __future__ import annotations
import ast, importlib, py_compile, traceback, io, datetime

def _ts():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def _log(msg, dbg_path=r"D:\ShrimpDev\debug_output.txt"):
    try:
        with open(dbg_path, "a", encoding="utf-8") as f:
            f.write(f"[GATE { _ts() }] {msg}\n")
    except Exception:
        print(f"[GATE { _ts() }] {msg}")

def smoke_compile(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        ast.parse(src)
        py_compile.compile(path, doraise=True)
        _log(f"SMOKE OK: {path}")
        return True, "OK"
    except Exception as e:
        _log(f"SMOKE FAIL: {path} :: {e}")
        return False, str(e)

def gate_try_import(fullname: str):
    try:
        importlib.invalidate_caches()
        mod = importlib.import_module(fullname)
        _log(f"IMPORT OK: {fullname}")
        return True, mod
    except Exception as e:
        buf = io.StringIO()
        traceback.print_exc(file=buf)
        _log(f"IMPORT FAIL: {fullname}\n{buf.getvalue()}")
        return False, buf.getvalue()
