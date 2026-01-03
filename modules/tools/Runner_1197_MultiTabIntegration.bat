# -*- coding: utf-8 -*-
"""
Runner_1197_MultiTabIntegration.py
- Fügt Agent- und Project-Tab modular hinzu
- Patcht main_gui.py idempotent, rückbaubar und Intake-schonend
- Schreibt neue Module: modules/module_code_agent.py, modules/module_code_project.py
"""
from __future__ import annotations
import re, sys
from pathlib import Path
import datetime as _dt

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "modules"
TOOLS = ROOT / "tools"
ARCH = ROOT / "_Archiv"
LOG = ROOT / "debug_output.txt"

def log(msg: str):
    msg = f"[R1197] {msg}"
    print(msg)
    with LOG.open("a", encoding="utf-8", newline="\n") as f:
        f.write(msg + "\n")

def backup(p: Path):
    ARCH.mkdir(exist_ok=True)
    ts = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = ARCH / f"{p.name}.{ts}.bak"
    bak.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")
    log(f"Backup: {bak}")

def write_file(p: Path, content: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8", newline="\n")
    log(f"Wrote: {p.relative_to(ROOT)}")

def ensure_agent_module():
    content = r'''# -*- coding: utf-8 -*-
"""
module_code_agent.py
Agent-Tab: Diagnose/Status/Logs – minimal, erweiterbar, Intake-kompatibel.
Kein Zugriff auf theme "background" (ttk), um TclError zu vermeiden.
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from typing import Optional

_PADX, _PADY = 8, 6

class _LED(ttk.Frame):
    """Kleine LED mit Label (status= 'ok'|'warn'|'fail'|'off')."""
    COLORS = {
        "ok":   "#2ecc71",
        "warn": "#f1c40f",
        "fail": "#e74c3c",
        "off":  "#95a5a6",
    }
    def __init__(self, master, text:str, status:str="off"):
        super().__init__(master)
        self._canvas = tk.Canvas(self, width=12, height=12, highlightthickness=0, bd=0)
        self._lbl = ttk.Label(self, text=text)
        self._canvas.grid(row=0, column=0, padx=(0,4))
        self._lbl.grid(row=0, column=1, sticky="w")
        self.set(status)

    def set(self, status:str):
        status = status if status in self.COLORS else "off"
        self._canvas.delete("all")
        self._canvas.create_oval(2,2,10,10, fill=self.COLORS[status], outline="")

def create_agent_tab(nb: ttk.Notebook) -> ttk.Frame:
    """Mountet Agent-Tab Inhalt und gibt das Root-Frame zurück."""
    root = ttk.Frame(nb)

    # --- LED-Leiste ---------------------------------------------------------
    ledbar = ttk.Frame(root)
    ledbar.pack(fill="x", padx=_PADX, pady=(_PADY, 0))
    leds = {
        "runner": _LED(ledbar, "Runner", "off"),
        "logs":   _LED(ledbar, "Logs",   "off"),
        "status": _LED(ledbar, "Status", "off"),
    }
    for i, w in enumerate(leds.values()):
        w.grid(row=0, column=i, padx=(0,10))

    # --- Tastenreihe --------------------------------------------------------
    btns = ttk.Frame(root)
    btns.pack(fill="x", padx=_PADX, pady=_PADY)
    ttk.Button(btns, text="Sanity-Check", width=16,
               command=lambda: leds["status"].set("ok")).grid(row=0, column=0, padx=3, pady=3)
    ttk.Button(btns, text="Logs öffnen", width=16,
               command=lambda: leds["logs"].set("ok")).grid(row=0, column=1, padx=3, pady=3)
    ttk.Button(btns, text="Runner testen", width=16,
               command=lambda: leds["runner"].set("ok")).grid(row=0, column=2, padx=3, pady=3)

    # --- Platz für spätere Widgets -----------------------------------------
    body = ttk.Label(root, text="Agent – bereit", anchor="w")
    body.pack(fill="both", expand=True, padx=_PADX, pady=_PADY)

    return root
'''
    write_file(MOD / "module_code_agent.py", content)

def ensure_project_module():
    content = r'''# -*- coding: utf-8 -*-
"""
module_code_project.py
Project-Tab: Build/Version/Changelog – Baseline UI, Intake-kompatibel.
"""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk

_PADX, _PADY = 8, 6

def create_project_tab(nb: ttk.Notebook) -> ttk.Frame:
    root = ttk.Frame(nb)

    top = ttk.Frame(root)
    top.pack(fill="x", padx=_PADX, pady=(_PADY,0))

    ttk.Label(top, text="Projektverwaltung").grid(row=0, column=0, sticky="w", padx=(0,10))
    ttk.Button(top, text="Changelog öffnen", width=18).grid(row=0, column=1, padx=3)
    ttk.Button(top, text="Build-Ordner", width=12).grid(row=0, column=2, padx=3)
    ttk.Button(top, text="Manifest erzeugen", width=18).grid(row=0, column=3, padx=3)

    tree = ttk.Treeview(root, columns=("version","date"), show="headings", height=12)
    tree.heading("version", text="Version")
    tree.heading("date", text="Datum")
    tree.column("version", width=120, anchor="w")
    tree.column("date", width=160, anchor="w")
    tree.pack(fill="both", expand=True, padx=_PADX, pady=_PADY)

    return root
'''
    write_file(MOD / "module_code_project.py", content)

def patch_main_gui():
    mg = ROOT / "main_gui.py"
    if not mg.exists():
        log("ERROR: main_gui.py nicht gefunden.")
        return 1

    src = mg.read_text(encoding="utf-8")

    # 1) Import-Block (idempotent)
    imp_block = (
        "# --- R1197: MultiTabIntegration imports (idempotent) ---\n"
        "try:\n"
        "    from modules.module_code_agent import create_agent_tab as _r1197_agent\n"
        "except Exception as _e:\n"
        "    _r1197_agent = None\n"
        "try:\n"
        "    from modules.module_code_project import create_project_tab as _r1197_project\n"
        "except Exception as _e:\n"
        "    _r1197_project = None\n"
        "# --- R1197 end ---\n"
    )
    if "R1197: MultiTabIntegration imports" not in src:
        # nach der ersten from/import-Zeile einfügen
        src = re.sub(r"(\nfrom\s+.+?\n)", r"\1" + imp_block, src, count=1, flags=re.M)

    # 2) Helper-Funktion (idempotent)
    helper = (
        "\n# --- R1197: MultiTabIntegration helpers ---\n"
        "def _r1197_safe_add_tab(nb, create_func, title):\n"
        "    import tkinter.ttk as _ttk\n"
        "    try:\n"
        "        if callable(create_func):\n"
        "            frm = create_func(nb)\n"
        "            nb.add(frm, text=title)\n"
        "        else:\n"
        "            f = _ttk.Frame(nb)\n"
        "            _ttk.Label(f, text=f\"{title} – bereit\").pack(padx=8, pady=6)\n"
        "            nb.add(f, text=title)\n"
        "    except Exception:\n"
        "        f = _ttk.Frame(nb)\n"
        "        _ttk.Label(f, text=f\"{title} – Fehler beim Laden.\", foreground=\"red\").pack(padx=8, pady=6)\n"
        "        nb.add(f, text=title)\n"
        "# --- R1197 end ---\n"
    )
    if "R1197: MultiTabIntegration helpers" not in src:
        src += helper

    # 3) Tabs hinzufügen (idempotent). Wir suchen eine Stelle, wo bereits Intake/Notebook existiert.
    # Strategie: vor dem finalen mainloop oder nach 'nb.pack' die Einfügung durchführen.
    add_block = (
        "\n# --- R1197: MultiTabIntegration mount ---\n"
        "try:\n"
        "    _r1197_safe_add_tab(nb, _r1197_agent, 'Agent')\n"
        "    _r1197_safe_add_tab(nb, _r1197_project, 'Project')\n"
        "except Exception:\n"
        "    pass\n"
        "# --- R1197 end ---\n"
    )
    if "R1197: MultiTabIntegration mount" not in src:
        # nach erstem Vorkommen von nb.pack( bzw. nb.grid(
        if re.search(r"\n\s*nb\.(pack|grid)\s*\(", src):
            src = re.sub(r"(\n\s*nb\.(?:pack|grid)\s*\(.+?\)\s*\n)",
                         r"\1" + add_block, src, count=1, flags=re.S)
        else:
            # Fallback: am Dateiende (besser als gar nicht)
            src += add_block

    # schreiben
    backup(mg)
    mg.write_text(src, encoding="utf-8", newline="\n")
    log("main_gui.py gepatcht (R1197).")
    return 0

def main():
    try:
        ensure_agent_module()
        ensure_project_module()
        rc = patch_main_gui()
        if rc != 0:
            return rc
        log("Runner done.")
        return 0
    except Exception as e:
        log(f"ERROR: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
