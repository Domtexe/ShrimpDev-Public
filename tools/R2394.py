# -*- coding: utf-8 -*-
from __future__ import annotations
from pathlib import Path
from datetime import datetime
import hashlib
import re

RID = "R2394"
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
TARGET = ROOT / "modules" / "ui_runner_products_tab.py"

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out = []
    out.append(f"# Report {RID} – ui_runner_products_tab Builder/Toplevel Scan (READ-ONLY)")
    out.append("")
    out.append(f"- Timestamp: {ts}")
    out.append(f"- Root: `{ROOT}`")
    out.append(f"- Target: `{TARGET}`")
    out.append("")

    if not TARGET.exists():
        out.append("## ERROR")
        out.append("- Target missing.")
        DOCS.mkdir(parents=True, exist_ok=True)
        rp = DOCS / f"Report_{RID}_Artefakte_Scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        rp.write_text("\n".join(out), encoding="utf-8")
        print(f"[{RID}] FEHLER: Report {rp}")
        return 2

    txt = TARGET.read_text(encoding="utf-8", errors="replace")
    lines = txt.splitlines()

    out.append(f"- Size: {TARGET.stat().st_size} bytes")
    out.append(f"- SHA256: `{sha256(TARGET)}`")
    out.append("")

    # Find builder defs (allow leading whitespace!)
    out.append("## Builder candidates")
    rx_def = re.compile(r"(?m)^\s*def\s+(build_[a-zA-Z0-9_]+)\s*\(")
    defs = [(m.group(1), m.start()) for m in rx_def.finditer(txt)]
    if not defs:
        out.append("_none_")
    else:
        for name, pos in defs:
            # line number
            lno = txt[:pos].count("\n") + 1
            out.append(f"- line {lno}: `{name}`")
    out.append("")

    # Focus: build_runner_products_tab
    out.append("## Focus: build_runner_products_tab")
    rx_focus = re.compile(r"(?m)^\s*def\s+build_runner_products_tab\s*\(")
    m = rx_focus.search(txt)
    if not m:
        out.append("- NOT FOUND")
        out.append("")
    else:
        lno = txt[:m.start()].count("\n") + 1
        out.append(f"- Found at line ~{lno}")
        out.append("")

    # Toplevel / geometry / center indicators
    pats = {
        "tk.Toplevel(": re.compile(r"\btk\.Toplevel\s*\("),
        "geometry(": re.compile(r"\bgeometry\s*\("),
        "screenwidth/height": re.compile(r"winfo_screenwidth|winfo_screenheight"),
        "center helper": re.compile(r"_center|center_window|CENTER_OVER_APP|zentrier"),
        "restored flag": re.compile(r"_restored_from_docking|restored_from_docking|restore_geometry"),
    }

    out.append("## Hits (Toplevel/Center/Geometry)")
    for label, rx in pats.items():
        hits = []
        for i, ln in enumerate(lines, start=1):
            if rx.search(ln):
                hits.append((i, ln.rstrip()))
        out.append(f"### {label}")
        if not hits:
            out.append("_none_")
        else:
            for i, ln in hits[:120]:
                out.append(f"- line {i}: `{ln}`")
            if len(hits) > 120:
                out.append(f"- ... ({len(hits)-120} more)")
        out.append("")

    DOCS.mkdir(parents=True, exist_ok=True)
    rp = DOCS / f"Report_{RID}_Artefakte_Scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    rp.write_text("\n".join(out), encoding="utf-8")
    print(f"[{RID}] OK: Report {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
