from __future__ import annotations
import json, tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
from .common_tabs import ensure_tab

ROOT = Path(r"D:\ShrimpDev")
CFG = ROOT / "config.json"


def _load() -> dict:
    if not CFG.exists():
        return {"workspace_root": r"D:\ShrimpHub", "quiet_mode": True}
    try:
        return json.loads(CFG.read_text(encoding="utf-8", errors="ignore") or "{}") or {}
    except Exception:
        return {"workspace_root": r"D:\ShrimpHub", "quiet_mode": True}


def _save(conf: dict):
    try:
        CFG.write_text(json.dumps(conf, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def _build_tab(parent):
    frm = ttk.Frame(parent)
    conf = _load()
    ttk.Label(frm, text="Workspace Root:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
    var_ws = tk.StringVar(value=conf.get("workspace_root", r"D:\ShrimpHub"))
    ttk.Entry(frm, textvariable=var_ws, width=46).grid(
        row=0, column=1, sticky="we", padx=6, pady=10
    )

    def _pick():
        d = filedialog.askdirectory(
            title="Workspace wählen", initialdir=str(Path(var_ws.get() or r"D:\\"))
        )
        if d:
            var_ws.set(d)

    ttk.Button(frm, text="...", command=_pick).grid(row=0, column=2)
    var_quiet = tk.BooleanVar(value=bool(conf.get("quiet_mode", True)))
    ttk.Checkbutton(frm, text="Quiet Mode (Popup-Reduktion)", variable=var_quiet).grid(
        row=1, column=1, sticky="w", padx=6
    )

    def _save_btn():
        conf["workspace_root"] = var_ws.get().strip() or r"D:\ShrimpHub"
        conf["quiet_mode"] = bool(var_quiet.get())
        _save(conf)
        try:
            messagebox.showinfo("ShrimpDev", "Gespeichert.")
        except Exception:
            pass

    ttk.Button(frm, text="Speichern", command=_save_btn).grid(
        row=2, column=1, sticky="e", padx=6, pady=12
    )
    return frm


def open_settings(app: tk.Tk) -> bool:
    try:
        return ensure_tab(app, "settings", "Settings", _build_tab)
    except Exception as ex:
        try:
            messagebox.showerror("ShrimpDev", f"Settings Fehler:\n{ex}")
        except Exception:
            pass
        return False
