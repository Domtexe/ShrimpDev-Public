from __future__ import annotations
import datetime, subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
LOG = ROOT / "debug_output.txt"


def _log(msg: str) -> None:
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    LOG.parent.mkdir(exist_ok=True, parents=True)
    with LOG.open("a", encoding="utf-8", newline="") as f:
        f.write(f"[RunnerBar {ts}] {msg}\n")


def _run_cmd(cmd_path: Path) -> None:
    if not cmd_path.exists():
        _log(f"SKIP: {cmd_path.name} nicht gefunden.")
        return
    try:
        _log(f"START: {cmd_path}")
        # Neues Konsolenfenster, blockiert GUI nicht
        creation = getattr(subprocess, "CREATE_NEW_CONSOLE", 0)
        subprocess.Popen([str(cmd_path)], cwd=str(TOOLS), creationflags=creation, shell=True)
    except Exception as ex:
        _log(f"ERROR: {ex!r}")


def build_runnerbar(parent: tk.Widget, mapping: dict[str, str] | None = None) -> ttk.Frame:
    """
    Erzeugt eine Button-Leiste für Runner .cmd-Dateien.
    mapping: {button_text: 'Rxxxx.cmd', ...}
    Buttons werden nur erstellt, wenn die .cmd existiert.
    """
    if mapping is None:
        mapping = {
            "Guard R9997": "R9997.cmd",
            "Fix R1351": "R1351.cmd",
            "Journal R1252": "R1252_LearningJournal.cmd",
            "Sanity R9999": "R9999.cmd",  # erscheint nur, wenn vorhanden
        }

    bar = ttk.Frame(parent)
    bar.grid_columnconfigure(999, weight=1)  # Stretch rechts

    c = 0
    for label, fname in mapping.items():
        cmd = TOOLS / fname
        if cmd.exists():
            b = ttk.Button(bar, text=label, command=lambda p=cmd: _run_cmd(p))
            b.grid(row=0, column=c, padx=(0, 6), pady=4, sticky="w")
            c += 1

    # wenn nichts existiert, trotzdem einen Hinweis anzeigen
    if c == 0:
        lab = ttk.Label(bar, text="Keine Runner gefunden (tools\\*.cmd).", foreground="#888")
        lab.grid(row=0, column=0, padx=0, pady=4, sticky="w")
    return bar
