from __future__ import annotations
import subprocess, tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
from .common_tabs import ensure_tab

ROOT = Path(r"D:\ShrimpDev")

def _list():
    t = ROOT/"tools"
    out=[]
    if t.exists():
        for p in sorted(t.glob("Runner_*.*")):
            if p.suffix.lower() in {".py",".bat",".cmd"}:
                out.append((p.name, p.suffix.lower().lstrip(".")))
    return out

def _build_tab(parent):
    frm = ttk.Frame(parent)
    bar = ttk.Frame(frm); bar.pack(fill="x", pady=6)
    ttk.Button(bar, text="Refresh", command=lambda: refresh()).pack(side="left")
    tree = ttk.Treeview(frm, columns=("file","type"), show="headings")
    for c,w in (("file",650),("type",160)): tree.heading(c, text=c); tree.column(c, width=w, anchor="w")
    tree.pack(fill="both", expand=True)

    def refresh():
        for i in tree.get_children(): tree.delete(i)
        for name, typ in _list(): tree.insert("", "end", values=(name, typ))
    def run_sel(_evt=None):
        sel = tree.focus()
        if not sel: return
        name, typ = tree.item(sel, "values")
        cmd = ["cmd","/c","start","", str(ROOT/"tools"/name)]
        try: subprocess.Popen(cmd, cwd=str(ROOT), shell=False)
        except Exception as ex:
            try: messagebox.showerror("ShrimpDev", f"Startfehler:\n{ex}")
            except Exception: pass
    tree.bind("<Double-1>", run_sel)
    refresh()
    return frm

def open_runner_board(app: tk.Tk) -> bool:
    try: return ensure_tab(app, "runners", "Runner Board", _build_tab)
    except Exception as ex:
        try: messagebox.showerror("ShrimpDev", f"Runner Board Fehler:\n{ex}")
        except Exception: pass
        return False
