"""
snippet_dev_intake_toolbar - R1177e/f (ShrimpDev ONLY)
- Grid-aware sichtbarer Mount: Toolbar in row=0; vorhandene Grid-Widgets -> +1 Row
- Fallback: pack(top) falls kein Grid verwendet wird
- Buttons: Analyse / Master-Sanity / Gate-Check / Logs / Runner
"""

from __future__ import annotations
from tkinter import ttk, messagebox


def _bind_or_warn(frame, method_name, fallback_text):
    fn = getattr(frame, method_name, None)
    if callable(fn):
        return fn

    def _fallback():
        try:
            messagebox.showinfo("Nicht verfügbar", fallback_text)
        except Exception:
            pass

    return _fallback


def _uses_grid(w):
    try:
        for child in w.winfo_children():
            if child.winfo_manager() == "grid":
                return True
    except Exception:
        pass
    return False


def _shift_grid_rows_down(w):
    try:
        for child in w.winfo_children():
            if child.winfo_manager() != "grid":
                continue
            info = child.grid_info()
            r = int(info.get("row", 0) or 0)
            c = int(info.get("column", 0) or 0)
            sticky = info.get("sticky", "")
            child.grid_forget()
            child.grid(row=r + 1, column=c, sticky=sticky)
    except Exception:
        pass


def attach_toolbar(frame) -> None:
    if getattr(frame, "_dev_toolbar_ready", False):
        return

    tb = ttk.Frame(frame)

    for text, mtd, fb in (
        ("Analyse jetzt", "_run_analysis", "Analyse-Handler fehlt in diesem Intake."),
        ("Master-Sanity", "_run_master_sanity", "Master-Sanity-Handler fehlt in diesem Intake."),
        ("Gate-Check", "_gate_check", "Gate-Check-Handler fehlt in diesem Intake."),
        ("Logs aktualisieren", "_restart_tail", "Log-Tail-Handler fehlt in diesem Intake."),
        (
            "Runner starten (neuester)",
            "_run_latest_runner",
            "Runner-Start-Handler fehlt in diesem Intake.",
        ),
    ):
        ttk.Button(tb, text=text, command=_bind_or_warn(frame, mtd, fb)).pack(
            side="left", padx=4, pady=4
        )

    if not hasattr(frame, "lbl_status"):
        frame.lbl_status = ttk.Label(frame, text="Bereit (Dev-Intake).", anchor="w")

    try:
        if _uses_grid(frame):
            _shift_grid_rows_down(frame)
            frame.grid_columnconfigure(0, weight=1)
            tb.grid(row=0, column=0, sticky="ew")
            if hasattr(frame, "lbl_status"):
                # sehr hohe row, damit die Statuszeile unten bleibt
                frame.lbl_status.grid(row=9999, column=0, sticky="ew")
        else:
            tb.pack(side="top", fill="x")
            if hasattr(frame, "lbl_status"):
                frame.lbl_status.pack(fill="x")
    except Exception:
        tb.pack(side="top", fill="x")
        if hasattr(frame, "lbl_status"):
            frame.lbl_status.pack(fill="x")

    frame._dev_toolbar_ready = True
