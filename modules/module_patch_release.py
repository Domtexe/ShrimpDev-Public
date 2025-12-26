from __future__ import annotations
import zipfile, tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import time
from .common_tabs import ensure_tab

ROOT = Path(r"D:\ShrimpDev")
OUT = ROOT / "_Exports"
OUT.mkdir(parents=True, exist_ok=True)


def _include(p: Path) -> bool:
    rel = p.relative_to(ROOT).as_posix()
    if rel.startswith("_Reports/") or rel.startswith("_Exports/") or rel.startswith("dist/"):
        return False
    if "/__pycache__/" in rel:
        return False
    return True


def _build_tab(parent):
    frm = ttk.Frame(parent)
    ttk.Label(frm, text="Erstellt ein ZIP der aktuellen ShrimpDev-Struktur.").pack(
        anchor="w", padx=10, pady=8
    )

    def build():
        name = f"ShrimpDev_patch_{time.strftime('%Y%m%d_%H%M%S')}.zip"
        target = OUT / name
        with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for p in ROOT.rglob("*"):
                if p.is_file() and _include(p):
                    z.write(p, p.relative_to(ROOT))
        try:
            messagebox.showinfo("ShrimpDev", f"Export:\n{target}")
        except Exception:
            pass

    ttk.Button(frm, text="Build ZIP", command=build).pack(pady=10)
    return frm


def open_patch_release(app: tk.Tk) -> bool:
    try:
        return ensure_tab(app, "patch", "Patch / Export", _build_tab)
    except Exception as ex:
        try:
            messagebox.showerror("ShrimpDev", f"Patch/Release Fehler:\n{ex}")
        except Exception:
            pass
        return False
