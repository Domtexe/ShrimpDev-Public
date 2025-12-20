# R2374A – Diagnose: Write-Pfade in config_manager
# READ-ONLY – keine Aenderungen
# Ziel: reale Schreibstellen identifizieren (kein Raten)

import os
import sys
import re
from datetime import datetime

RID = "R2374A"

WRITE_HINTS = [
    (r"\.write\s*\(", "write() call"),
    (r"\.save\s*\(", "save() call"),
    (r"open\s*\(.*['\"]w['\"]", "open(...,'w')"),
    (r"open\s*\(.*['\"]a['\"]", "open(...,'a')"),
    (r"configparser", "configparser usage"),
]

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log(msg):
    print("[" + RID + "] " + ts() + " " + msg)

def root_dir():
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.abspath(os.path.join(here, ".."))

def read_lines(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.readlines()

def main():
    root = root_dir()
    cm_path = os.path.join(root, "modules", "config_manager.py")
    docs = os.path.join(root, "docs")
    os.makedirs(docs, exist_ok=True)

    if not os.path.isfile(cm_path):
        log("FEHLER: config_manager.py nicht gefunden")
        return 2

    lines = read_lines(cm_path)
    findings = []

    current_func = "<module-level>"
    for idx, line in enumerate(lines, start=1):
        m = re.match(r"\s*def\s+([a-zA-Z0-9_]+)\s*\(", line)
        if m:
            current_func = m.group(1)

        for pat, label in WRITE_HINTS:
            if re.search(pat, line):
                findings.append({
                    "line": idx,
                    "func": current_func,
                    "label": label,
                    "code": line.rstrip()
                })

    # Write analysis doc
    out = []
    out.append("# ConfigManager – Write Path Analyse\n\n")
    out.append("- Zeit: " + ts() + "\n")
    out.append("- Datei: modules/config_manager.py\n\n")

    if not findings:
        out.append("## Ergebnis\n\n")
        out.append("❗ Keine potentiellen Schreibstellen gefunden.\n")
    else:
        out.append("## Gefundene potentielle Schreibstellen\n\n")
        for f in findings:
            out.append("### Funktion: `" + f["func"] + "`\n")
            out.append("- Zeile: " + str(f["line"]) + "\n")
            out.append("- Typ: " + f["label"] + "\n")
            out.append("```python\n" + f["code"] + "\n```\n\n")

    md_path = os.path.join(docs, "ConfigManager_WritePaths.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("".join(out))

    # Report
    rep = []
    rep.append("# " + RID + " – Diagnose Report\n\n")
    rep.append("- Zeit: " + ts() + "\n")
    rep.append("- Treffer gesamt: " + str(len(findings)) + "\n\n")
    rep.append("## Naechster Schritt\n")
    rep.append("- R2374B: gezielte Delegation der **konkreten** Schreibpfade\n")
    rep.append("- Keine Regex-Substitution auf Vermutung\n")

    rep_path = os.path.join(docs, "Report_" + RID + "_ConfigManager_Diagnose.md")
    with open(rep_path, "w", encoding="utf-8") as f:
        f.write("".join(rep))

    log("OK: Analyse geschrieben: " + md_path)
    log("OK: Report geschrieben: " + rep_path)
    return 0

if __name__ == "__main__":
    sys.exit(main())
