"""
BAT-First Runner Executor für ShrimpDev:
- Startet bevorzugt .bat
- Erzeugt fehlende .bat automatisch (neben tools\Runner_XXXX.py)
- Nicht-blockierend (Thread), zentrale Logs + Reportdatei

API:
    run(runner_py: str, *, timeout_sec: int = 0, title: str | None = None) -> dict
"""

from __future__ import annotations
import os, subprocess, threading, time, traceback
from datetime import datetime
from typing import Any
from modules.exception_logger import (
    log_runner_start,
    log_runner_end,
    log_runner_output,
)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TOOLS = os.path.join(ROOT, "tools")
REPORTS = os.path.join(ROOT, "_Reports")
LOGFILE = os.path.join(ROOT, "debug_output.txt")

# --- Runner Busy Flag (R2427) ---
RUNNER_BUSY = False


def is_runner_busy() -> bool:
    return bool(RUNNER_BUSY)


# --------------------------------


def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _log(msg: str) -> None:
    os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)
    with open(LOGFILE, "a", encoding="utf-8", newline="") as f:
        f.write(msg.rstrip() + "\n")


def _norm_rel(path: str) -> str:
    try:
        return os.path.normpath(os.path.relpath(path, ROOT))
    except Exception:
        return path


def _ensure_reports() -> None:
    os.makedirs(REPORTS, exist_ok=True)


def _bat_template(rel_runner_py: str, window_title: str) -> str:
    return f"""@echo off
setlocal EnableExtensions EnableDelayedExpansion
title {window_title}

pushd "%~dp0"
cd ..
set "ROOT=%CD%"
echo [CWD] %ROOT%

set "PYEXE=py -3"
for /f "delims=" %%P in ('where py 2^>nul') do (set "PYFOUND=1")
if not defined PYFOUND (
  for /f "delims=" %%P in ('where python 2^>nul') do (set "PYEXE=python")
)

echo [RUN ] %PYEXE% -u {rel_runner_py}
%PYEXE% -u {rel_runner_py}
set "RC=!ERRORLEVEL!"
echo [END ] RC=!RC!
echo.
pause
endlocal
"""


def _ensure_bat_for_runner(runner_py_abs: str, *, title: str | None) -> str:
    if not os.path.isabs(runner_py_abs):
        runner_py_abs = os.path.join(ROOT, runner_py_abs)
    if not os.path.exists(runner_py_abs):
        raise FileNotFoundError(f"Runner-Python nicht gefunden: {runner_py_abs}")

    base = os.path.splitext(os.path.basename(runner_py_abs))[0]
    bat_abs = os.path.join(TOOLS, base + ".bat")
    if not os.path.exists(bat_abs):
        rel_py = _norm_rel(runner_py_abs)
        with open(bat_abs, "w", encoding="utf-8", newline="") as f:
            f.write(_bat_template(rel_py, title or f"ShrimpDev - {base}"))
        _log(f"[RunnerExec] {_ts()} BAT erzeugt: {_norm_rel(bat_abs)}")
    else:
        _log(f"[RunnerExec] {_ts()} BAT vorhanden: {_norm_rel(bat_abs)}")
    return bat_abs


def _run_sync(cmd: list[str], *, timeout_sec: int) -> dict[str, Any]:
    start = time.time()
    try:
        p = subprocess.Popen(
            cmd,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
        )
        out, _ = p.communicate(timeout=timeout_sec if timeout_sec > 0 else None)
        rc = p.returncode
    except subprocess.TimeoutExpired:
        p.kill()
        out, rc = ("[TIMEOUT]\n", 124)
    except Exception:
        out, rc = (traceback.format_exc(), 99)
    return {"rc": rc, "output": out or "", "duration": time.time() - start}


def run(runner_py: str, *, timeout_sec: int = 0, title: str | None = None) -> dict[str, Any]:
    """
    Startet runner_py via .bat (wird bei Bedarf generiert), nicht-blockierend.
    Gibt {thread, report_path, bat_path} zurück.
    """
    _ensure_reports()
    runner_py_abs = runner_py if os.path.isabs(runner_py) else os.path.join(ROOT, runner_py)
    bat_abs = _ensure_bat_for_runner(runner_py_abs, title=title)

    base = os.path.splitext(os.path.basename(runner_py_abs))[0]
    report_path = os.path.join(REPORTS, f"{base}_gui_capture.txt")

    def _worker():
        global RUNNER_BUSY
        RUNNER_BUSY = True
        _log(f"[RunnerExec] {_ts()} START {_norm_rel(bat_abs)} (timeout={timeout_sec}s)")
        log_runner_start(base, title or "")
        res = _run_sync([bat_abs], timeout_sec=timeout_sec)
        log_runner_output(base, res.get("output", ""))
        with open(report_path, "w", encoding="utf-8", newline="") as f:
            f.write(res["output"])
        _log(
            f"[RunnerExec] {_ts()} ENDE RC={res['rc']} Dauer={res['duration']:.2f}s Report={_norm_rel(report_path)}"
        )
        log_runner_end(base, res.get("rc", -1))
        RUNNER_BUSY = False

    t = threading.Thread(target=_worker, name=f"RunnerExec-{base}", daemon=True)
    t.start()
    return {"thread": t, "report_path": report_path, "bat_path": bat_abs}


# R1167g: safe _log wrapper (append, no-replace)
# Diese Neudefinition überschreibt die vorherige _log()-Funktion sicher.
def _log(msg: str) -> None:  # noqa: F811 (absichtliche Neudefinition)
    try:
        # Sicherstellen, dass LOGFILE-Verzeichnis existiert, Fehler still tolerieren
        try:
            os.makedirs(os.path.dirname(LOGFILE), exist_ok=True)
        except Exception:
            pass
        # Best-effort schreiben; Import im GUI darf niemals crashen
        try:
            with open(LOGFILE, "a", encoding="utf-8", newline="") as f:
                f.write((msg or "").rstrip() + "\n")
        except Exception:
            pass
    except Exception:
        pass


# R2249_CENTRAL_RUNNER_LOGGING
def _r2249_append_debug(root: Path, line: str) -> None:
    try:
        p = root / "debug_output.txt"
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("a", encoding="utf-8", errors="replace", newline="\n") as f:
            f.write(line.rstrip("\n") + "\n")
    except Exception:
        pass


def _r2249_log_end(runner_id: str, title: str, exit_code: int, stdout_tail: str = "") -> None:
    try:
        _root = Path(__file__).resolve().parents[1]
        line = (
            f"[{now_str()}] [RUNNER] END {runner_id}"
            + (f" | {title}" if title else "")
            + f" | exit={exit_code}"
        )
        if hasattr(exception_logger, "log_runner_end"):
            exception_logger.log_runner_end(runner_id, title, exit_code, stdout_tail)
        else:
            _r2249_append_debug(_root, line)
    except Exception:
        pass
