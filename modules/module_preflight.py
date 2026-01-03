from __future__ import annotations
import sys, tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import time
from .common_tabs import ensure_tab

ROOT = Path(r"D:\ShrimpDev")
OUT = ROOT / "_Reports" / "Preflight"
OUT.mkdir(parents=True, exist_ok=True)


def _checks():
    rows = []
    rows.append(("python", sys.version.split()[0], "OK" if sys.version_info >= (3, 10) else "WARN"))
    try:
        rows.append(("tkinter", "available", "OK"))
    except Exception as ex:
        rows.append(("tkinter", f"error: {ex}", "FAIL"))
    for d in (ROOT / "modules", ROOT / "tools", ROOT / "_Reports"):
        rows.append(
            (f"dir:{d.name}", "exists" if d.exists() else "missing", "OK" if d.exists() else "WARN")
        )
    return rows


def _build_tab(parent):
    frm = ttk.Frame(parent)
    b = ttk.Frame(frm)
    b.pack(fill="x", pady=6)
    tree = ttk.Treeview(frm, columns=("item", "value", "status"), show="headings")
    for c, w in zip(("item", "value", "status"), (300, 280, 80)):
        tree.heading(c, text=c)
        tree.column(c, width=w, anchor="w")
    tree.pack(fill="both", expand=True)

    def run():
        rows = _checks()
        for i in tree.get_children():
            tree.delete(i)
        for r in rows:
            tree.insert("", "end", values=r)
        rep = OUT / f"Preflight_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        rep.write_text("\n".join([f"{a}\t{b}\t{c}" for a, b, c in rows]), encoding="utf-8")

    ttk.Button(b, text="Run Checks", command=run).pack(side="right", padx=10)
    run()
    return frm


def open_preflight(app: tk.Tk) -> bool:
    try:
        return ensure_tab(app, "preflight", "Preflight", _build_tab)
    except Exception as ex:
        try:
            messagebox.showerror("ShrimpDev", f"Preflight Fehler:\n{ex}")
        except Exception:
            pass
        return False
