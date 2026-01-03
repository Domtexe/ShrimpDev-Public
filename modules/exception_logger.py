# exception_logger.py - central exception logging (no triple-quotes)
from __future__ import annotations

import sys
import traceback
from datetime import datetime
from pathlib import Path

_INSTALLED = False
_ROOT = None
_DEBUG_FILE = None


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _safe_write(path: Path, text: str) -> None:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8", errors="replace") as f:
            f.write(text)
            if not text.endswith("\n"):
                f.write("\n")
    except Exception:
        pass


def configure(project_root: str | Path) -> None:
    global _ROOT, _DEBUG_FILE
    _ROOT = Path(project_root).resolve()
    _DEBUG_FILE = _ROOT / "debug_output.txt"


def log_exception(exc: BaseException, context: str = "") -> None:
    try:
        tb = traceback.format_exc()
        if not tb or tb.strip() == "NoneType: None":
            tb = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))
    except Exception:
        tb = "traceback unavailable"

    ctx = context.strip()
    head = f"[{_now()}] EXCEPTION" + (f" ({ctx})" if ctx else "")
    payload = head + "\n" + tb.strip() + "\n"

    if _DEBUG_FILE is not None:
        _safe_write(_DEBUG_FILE, payload)


def _sys_excepthook(exctype, value, tb) -> None:
    try:
        txt = "".join(traceback.format_exception(exctype, value, tb))
        head = f"[{_now()}] UNCAUGHT"
        payload = head + "\n" + txt.strip() + "\n"
        if _DEBUG_FILE is not None:
            _safe_write(_DEBUG_FILE, payload)
    except Exception:
        pass
    try:
        sys.__excepthook__(exctype, value, tb)
    except Exception:
        pass


def _install_tk_report_callback() -> None:
    try:
        import tkinter as tk
    except Exception:
        return

    orig = getattr(tk.Tk, "report_callback_exception", None)

    def _wrapped(self, exc, val, tb):
        try:
            txt = "".join(traceback.format_exception(exc, val, tb))
            head = f"[{_now()}] TK_CALLBACK"
            payload = head + "\n" + txt.strip() + "\n"
            if _DEBUG_FILE is not None:
                _safe_write(_DEBUG_FILE, payload)
        except Exception:
            pass
        if orig:
            try:
                return orig(self, exc, val, tb)
            except Exception:
                return None
        return None

    try:
        tk.Tk.report_callback_exception = _wrapped
    except Exception:
        pass


def install(project_root: str | Path) -> None:
    global _INSTALLED
    if _INSTALLED:
        return
    configure(project_root)
    try:
        sys.excepthook = _sys_excepthook
    except Exception:
        pass
    _install_tk_report_callback()
    _INSTALLED = True


# ---------------------------------------------------------------------------
# Central Log API (R2226)
# Ziel: Eine zentrale API, die sowohl GUI-Events als auch Runner-Output in
# debug_output.txt schreibt. Bestehendes Exception-Logging bleibt unverändert.
# ---------------------------------------------------------------------------
def _fmt_line(level: str, source: str, message: str) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lvl = (level or "INFO").strip().upper()
    src = (source or "APP").strip()
    msg = (message or "").rstrip("\n")
    return f"[{now}] [{lvl}] [{src}] {msg}\n"


def log_event(source: str, message: str, level: str = "INFO") -> None:
    try:
        _safe_write(
            (
                _DEBUG_FILE
                if _DEBUG_FILE is not None
                else (
                    (_ROOT / "debug_output.txt")
                    if _ROOT is not None
                    else (Path(__file__).resolve().parents[1] / "debug_output.txt")
                )
            ),
            _fmt_line(level, source, message),
        )
    except Exception:
        pass


def log_runner_start(runner_id: str, label: str = "") -> None:
    rid = (runner_id or "").strip()
    lbl = (label or "").strip()
    msg = f"Runner START rid={rid} label={lbl}" if lbl else f"Runner START rid={rid}"
    log_event("RUNNER", msg, "INFO")


def log_runner_end(runner_id: str, exit_code: int) -> None:
    rid = (runner_id or "").strip()
    log_event("RUNNER", f"Runner END rid={rid} exit={exit_code}", "INFO")


def log_runner_output(runner_id: str, text: str, stream: str = "STDOUT") -> None:
    rid = (runner_id or "").strip()
    st = (stream or "STDOUT").strip().upper()
    if text is None:
        return
    s = str(text)
    if not s:
        return
    # Split into lines to keep log readable; preserve order.
    for ln in s.splitlines():
        log_event("RUNNER", f"{rid} {st}: {ln}", "INFO")


# === RUNNER_LOG_API_BEGIN ===
from pathlib import Path as _Path
from datetime import datetime as _dt


def _runner_log_path() -> _Path:
    # HARTE Wahrheit: immer Projektroot\debug_output.txt
    # __file__ = ...\modules\exception_logger.py
    try:
        return _Path(__file__).resolve().parents[1] / "debug_output.txt"
    except Exception:
        # worst-case fallback
        return _Path("debug_output.txt").resolve()


def _runner_append(line: str) -> None:
    # Kein _safe_write, kein swallow: direkte Datei
    p = _runner_log_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8", errors="replace", newline="\n") as f:
        f.write(line + "\n")
        try:
            f.flush()
        except Exception:
            pass


def _runner_now() -> str:
    try:
        return _dt.now().strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return "????-??-?? ??:??:??"


def log_runner_start(runner_id: str, label: str = "") -> None:
    rid = str(runner_id)
    lab = str(label).strip()
    msg = f"[{_runner_now()}] [RUNNER] START {rid}" + (f" | {lab}" if lab else "")
    _runner_append(msg)


def log_runner_output(runner_id: str, text: str, stream: str = "STDOUT") -> None:
    rid = str(runner_id)
    st = str(stream).strip() or "STDOUT"
    msg = "" if text is None else str(text)
    if not msg:
        return
    for line in msg.splitlines():
        _runner_append(f"[{_runner_now()}] [RUNNER] {rid} {st}: {line}")


def log_runner_end(runner_id: str, exit_code: int | str = 0) -> None:
    rid = str(runner_id)
    code = str(exit_code)
    _runner_append(f"[{_runner_now()}] [RUNNER] END {rid} | exit={code}")


# === RUNNER_LOG_API_END ===
