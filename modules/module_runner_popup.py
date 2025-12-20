"""
module_runner_popup - zentrales Runner-Ausgabe-Popup für ShrimpDev

Features:
- Zentrales Popup für .cmd-Runner ohne blinkendes CMD
- Live-Output mit Auto-Scroll (abschaltbar)
- Farbige Hervorhebung:
    * OK   (Exitcode 0)           -> grün
    * WARN-Zeilen ("WARN", ...)   -> orange
    * ERROR/Fehler                -> rot
- Titelstatus: (OK) / (WARN) / (ERROR)
- Buttons: "Text kopieren", "Kopieren und schließen", "Schließen"
"""

from __future__ import annotations

import subprocess
import sys
import threading
from pathlib import Path
from typing import Optional, Union

import tkinter as tk
from tkinter import ttk
import os
import re
from tkinter import messagebox


# Flag für "kein Fenster" unter Windows
if sys.platform.startswith("win"):
    CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)
else:
    CREATE_NO_WINDOW = 0


def _append_text(
    text_widget: tk.Text,
    text: str,
    auto_scroll: bool = True,
    tag: Optional[str] = None,
) -> None:
    """
    Text anhängen und optional mit einem Tag versehen.

    Strategie:
    - Text immer am Ende einfügen.
    - Danach wird die LETZTE Zeile markiert:
        start = "end-1l linestart"
        end   = "end-1c"
      -> so färben wir nur die frische Zeile, ohne ältere Zeilen zu erwischen.
    """
    if not text_widget.winfo_exists():
        return

    text_widget.configure(state="normal")

    # Text ans Ende schreiben
    text_widget.insert("end", text)

    # Nur wenn ein Tag gesetzt werden soll, markieren wir die letzte Zeile
    if tag:
        try:
            line_start = text_widget.index("end-1l linestart")
            line_end = text_widget.index("end-1c")
            text_widget.tag_add(tag, line_start, line_end)
        except Exception:
            pass

    if auto_scroll:
        text_widget.see("end")

    text_widget.configure(state="disabled")


def _center_window(win: tk.Toplevel) -> None:
    """
    Zentriere ein Toplevel über seinem Master (oder Bildschirm).
    """
    win.update_idletasks()

    master = win.master
    try:
        if master is not None and master.winfo_exists():
            master.update_idletasks()
            mw = master.winfo_width()
            mh = master.winfo_height()
            mx = master.winfo_rootx()
            my = master.winfo_rooty()
        else:
            mw = win.winfo_screenwidth()
            mh = win.winfo_screenheight()
            mx = 0
            my = 0
    except Exception:
        mw = win.winfo_screenwidth()
        mh = win.winfo_screenheight()
        mx = 0
        my = 0

    ww = win.winfo_width()
    wh = win.winfo_height()

    x = mx + (mw - ww) // 2
    y = my + (mh - wh) // 2

    win.geometry("+{}+{}".format(x, y))


def _start_runner_thread(
    cmd_path: Path,
    text_widget: tk.Text,
    append_fn=None,
    on_finished=None,
) -> None:
    """
    Startet den Runner in einem Hintergrundthread und streamt die Ausgabe ins Textfeld.
    """

    def default_append(msg: str) -> None:
        try:
            _append_text(text_widget, msg, True, None)
        except Exception:
            pass

    def worker() -> None:
        fn = append_fn or default_append

        try:
            cmd = ["cmd", "/c", str(cmd_path)]
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                creationflags=CREATE_NO_WINDOW,
            )
        except Exception as exc:
            text_widget.after(0, fn, "Fehler beim Starten des Runners:\n{}\n".format(exc))
            if on_finished is not None:
                text_widget.after(0, lambda rc=-1: on_finished(rc))
            return

        if proc.stdout is not None:
            for line in proc.stdout:
                text_widget.after(0, fn, line)

        rc = proc.wait()
        text_widget.after(0, fn, "\n[Runner beendet mit Code {}]\n".format(rc))
        if on_finished is not None:
            text_widget.after(0, lambda rc=rc: on_finished(rc))

    t = threading.Thread(target=worker, daemon=True)
    t.start()


def run_runner_with_popup(app, path: str) -> None:
    """Runner-Ausgabe-Popup: Status links, Auto-Scroll unten links, Buttons zentriert."""
    try:
        if not path:
            return
        cmd_path = Path(path)
        if not cmd_path.exists():
            return

        base = cmd_path.name
        rid = base
        try:
            m = re.search(r"\bR(\d{3,6}[a-zA-Z]?)\b", base)
            if m:
                rid = "R" + m.group(1)
            else:
                rid = os.path.splitext(base)[0]
        except Exception:
            pass

        master = app if app is not None else None
        win = tk.Toplevel(master)
        win.title(f"{rid} – Runner Output")
        try:
            if master is not None:
                win.transient(master)  # zentral über ShrimpDev
        except Exception:
            pass
        try:
            win.lift()
            win.focus_force()
        except Exception:
            pass

        try:
            win.geometry("1000x650")
        except Exception:
            pass

        outer = ttk.Frame(win, padding=8)
        outer.pack(fill="both", expand=True)

        # TOP: Status links (wie gewünscht)
        top = ttk.Frame(outer)
        top.pack(fill="x")
        lbl_status = ttk.Label(top, text="RUNNING")
        lbl_status.pack(side="left")

        # MID: Text + Scroll
        mid = ttk.Frame(outer)
        mid.pack(fill="both", expand=True, pady=(8, 0))

        yscroll = ttk.Scrollbar(mid, orient="vertical")
        yscroll.pack(side="right", fill="y")

        txt = tk.Text(mid, wrap="word", yscrollcommand=yscroll.set)
        txt.pack(side="left", fill="both", expand=True)
        yscroll.configure(command=txt.yview)
        txt.configure(state="disabled")

        var_auto = tk.BooleanVar(value=True)

        # Buttons / Clipboard
        def _copy_all():
            try:
                win.clipboard_clear()
                win.clipboard_append(txt.get("1.0", "end"))
            except Exception:
                pass

        def _close():
            try:
                win.destroy()
            except Exception:
                pass

        def _copy_and_close():
            _copy_all()
            _close()

        win.protocol("WM_DELETE_WINDOW", _close)

        # Logging
        try:
            from modules import exception_logger as _elog
        except Exception:
            _elog = None

        state = {"warn": False, "err": False}

        def _set_status(tag: str) -> None:
            try:
                lbl_status.configure(text=tag)
            except Exception:
                pass
            try:
                win.title(f"{rid} – Runner Output ({tag})")
            except Exception:
                pass

        def _classify(line: str):
            s = (line or "").strip().lower()
            if not s:
                return None
            if "traceback" in s or "error" in s or "exception" in s or "fehler" in s:
                return "ERR"
            if "warn" in s:
                return "WARN"
            return None

        def _log_start():
            try:
                if _elog is not None:
                    _elog.log_runner_start(str(rid), base)
            except Exception:
                pass

        def _log_line(line: str):
            try:
                if _elog is not None:
                    _elog.log_runner_output(str(rid), str(line).rstrip("\n"), "STDOUT")
            except Exception:
                pass

        def _log_end(rc: int):
            try:
                if _elog is not None:
                    _elog.log_runner_end(str(rid), int(rc))
            except Exception:
                pass

        def append_fn(msg: str) -> None:
            _log_line(msg)
            c = _classify(msg)
            if c == "WARN":
                state["warn"] = True
            if c == "ERR":
                state["err"] = True
            try:
                _append_text(txt, msg, bool(var_auto.get()), None)
            except Exception:
                try:
                    # falls _append_text nur 3 Parameter kann
                    _append_text(txt, msg, bool(var_auto.get()))
                except Exception:
                    pass

        def on_finished(rc: int):
            _log_end(rc)
            if rc != 0 or state["err"]:
                _set_status("ERROR")
            elif state["warn"]:
                _set_status("WARN")
            else:
                _set_status("OK")

        # Header
        try:
            _append_text(txt, f"{cmd_path}\n\n", True, None)
        except Exception:
            try:
                _append_text(txt, f"{cmd_path}\n\n", True)
            except Exception:
                pass

        # BOTTOM: Auto-Scroll links + Buttons zentriert
        bottom = ttk.Frame(outer)
        bottom.pack(fill="x", pady=(8, 0))

        # Grid: [Auto] [spacer] [Buttons...] [spacer]
        bottom.columnconfigure(0, weight=0)
        bottom.columnconfigure(1, weight=1)
        bottom.columnconfigure(2, weight=0)
        bottom.columnconfigure(3, weight=0)
        bottom.columnconfigure(4, weight=0)
        bottom.columnconfigure(5, weight=1)

        ttk.Checkbutton(bottom, text="Auto-Scroll", variable=var_auto).grid(
            row=0, column=0, sticky="w", padx=(0, 10)
        )

        ttk.Button(bottom, text="Text kopieren", command=_copy_all).grid(row=0, column=2, padx=4)
        ttk.Button(bottom, text="Kopieren & schließen", command=_copy_and_close).grid(row=0, column=3, padx=4)
        ttk.Button(bottom, text="Schließen", command=_close).grid(row=0, column=4, padx=4)

        _set_status("RUNNING")
        _log_start()
        _start_runner_thread(cmd_path, txt, append_fn=append_fn, on_finished=on_finished)

        try:
            _center_window(win)
        except Exception:
            pass

    except Exception:
        return
