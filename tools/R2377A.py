# R2377A – Docking Restore CODE DIAG (READ-ONLY)
# Analysiert restore_from_ini(): Blockstruktur + Einrückungen
# KEINE Code-Änderung, nur Report.

import os
import sys
from datetime import datetime

RID = "R2377A"
TS = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def root_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def log(msg):
    print(f"[{RID}] {datetime.now():%H:%M:%S} {msg}")

def main():
    root = root_dir()
    path = os.path.join(root, "modules", "module_docking.py")
    rep_dir = os.path.join(root, "docs")
    os.makedirs(rep_dir, exist_ok=True)
    rep = os.path.join(rep_dir, f"Report_{RID}_Restore_Code_Diag.md")

    if not os.path.isfile(path):
        log("FEHLER: module_docking.py nicht gefunden")
        return 2

    lines = open(path, "r", encoding="utf-8", errors="replace").read().splitlines()

    start = None
    for i, ln in enumerate(lines):
        if ln.strip() == "def restore_from_ini(self):":
            start = i
            break

    if start is None:
        log("FEHLER: restore_from_ini nicht gefunden")
        return 2

    # collect until next top-level def with same indent
    base_indent = len(lines[start]) - len(lines[start].lstrip())
    block = []
    for j in range(start, len(lines)):
        ln = lines[j]
        indent = len(ln) - len(ln.lstrip())
        if j > start and indent <= base_indent and ln.lstrip().startswith("def "):
            break
        block.append((j+1, indent, ln.rstrip()))

    out = []
    out.append(f"# {RID} – Restore-Code Diagnose\n")
    out.append(f"- Zeit: {TS}")
    out.append(f"- Datei: modules/module_docking.py\n")
    out.append("## restore_from_ini – Struktur\n")
    out.append(f"- Startzeile: {start+1}")
    out.append(f"- Basis-Indent: {base_indent}\n")
    out.append("```text")
    for lineno, indent, text in block:
        out.append(f"{lineno:>4} | {' ' * indent}{text}")
    out.append("```")
    out.append("\n## Hinweise")
    out.append("- READ-ONLY Diagnose")
    out.append("- Dient als Grundlage für **exakt platzierte** Fixes (R2377B)")
    out.append("- Keine Aussagen über Verhalten, nur Struktur\n")

    with open(rep, "w", encoding="utf-8") as f:
        f.write("\n".join(out))

    log(f"OK: Report geschrieben: {rep}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
