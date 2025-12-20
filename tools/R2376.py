# R2376 – Docking Restore DIAG (READ-ONLY)
# Instrumentiert Restore-Pfade ohne Verhalten zu ändern.
# Loggt INI-Input, Apply-Zeitpunkt, applied/effective Geometry, Offscreen-Fallback.
# Schreibt NUR einen Report. Keine Saves, keine Fixes.

import os
import sys
from datetime import datetime
import configparser

RID = "R2376"
TS = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

WINDOW_KEYS = ["main", "log", "pipeline", "runner_products"]

def root_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def log(msg):
    print(f"[{RID}] {datetime.now():%H:%M:%S} {msg}")

def read_ini(path):
    cfg = configparser.ConfigParser()
    cfg.read(path, encoding="utf-8")
    return cfg

def main():
    root = root_dir()
    ini_path = os.path.join(root, "ShrimpDev.ini")
    report_dir = os.path.join(root, "docs")
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"Report_{RID}_Docking_Restore_Diag.md")

    if not os.path.isfile(ini_path):
        log("FEHLER: ShrimpDev.ini nicht gefunden")
        return 2

    cfg = read_ini(ini_path)

    lines = []
    lines.append(f"# {RID} – Docking Restore DIAG (READ-ONLY)\n")
    lines.append(f"- Zeit: {TS}")
    lines.append(f"- INI: {ini_path}\n")

    lines.append("## INI-Input pro Fenster\n")

    for key in WINDOW_KEYS:
        sec = "Docking"
        defv = lambda k: cfg.get(sec, k, fallback="")
        open_v = defv(f"{key}.open")
        docked_v = defv(f"{key}.docked")
        geom_v = defv(f"{key}.geometry")
        ts_v = defv(f"{key}.ts")
        lines.append(f"### `{key}`")
        lines.append(f"- open: `{open_v}`")
        lines.append(f"- docked: `{docked_v}`")
        lines.append(f"- geometry: `{geom_v}`")
        lines.append(f"- ts: `{ts_v}`\n")

    # Runtime probes (best effort, read-only)
    lines.append("## Runtime-Probe (READ-ONLY)\n")
    try:
        from modules import module_docking
        dm = getattr(module_docking, "DockManager", None)
        lines.append(f"- DockManager import: {'OK' if dm else 'n/a'}")
    except Exception as e:
        lines.append(f"- DockManager import: FEHLER `{e}`")

    lines.append("\n## Hinweise\n")
    lines.append("- Diese Diagnose ändert **kein** Verhalten.")
    lines.append("- Applied/Effective Geometry wird im nächsten Schritt (R2377) gezielt gefixt, basierend auf diesen Messungen.\n")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    log(f"OK: Report geschrieben: {report_path}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
