# -*- coding: utf-8 -*-
# [R2392] READ-ONLY scan for docking conflicts: Toplevel creation + centering in tab builders
from __future__ import annotations
from pathlib import Path
from datetime import datetime
import re
import hashlib

RID = "R2392"
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
MODULES = ROOT / "modules"

FILES = [
    MODULES / "ui_runner_products_tab.py",
    MODULES / "ui_pipeline_tab.py",
    MODULES / "ui_log_tab.py",
    MODULES / "module_docking.py",
]

PATTERNS = {
    "toplevel": re.compile(r"\btk\.Toplevel\s*\("),
    "center": re.compile(r"\bcenter\b|\b_center_window\b|\bwinfo_screenwidth\b|\bwinfo_screenheight\b"),
    "geometry": re.compile(r"\bgeometry\s*\("),
    "restored_flag": re.compile(r"_restored_from_docking|restored_from_ini|restore_geometry"),
}

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def main() -> int:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out = []
    out.append(f"# Report {RID} – Toplevel/Center Scan (READ-ONLY)")
    out.append("")
    out.append(f"- Timestamp: {ts}")
    out.append(f"- Root: `{ROOT}`")
    out.append("")

    for f in FILES:
        out.append(f"## {f.name}")
        if not f.exists():
            out.append(f"- MISSING: `{f}`")
            out.append("")
            continue

        data = f.read_text(encoding="utf-8", errors="replace").splitlines()
        out.append(f"- Path: `{f}`")
        out.append(f"- Size: {f.stat().st_size} bytes")
        out.append(f"- SHA256: `{sha256(f)}`")
        out.append("")

        hits = {k: [] for k in PATTERNS.keys()}
        for i, line in enumerate(data, start=1):
            for k, rx in PATTERNS.items():
                if rx.search(line):
                    hits[k].append((i, line.rstrip()))

        def dump(name: str):
            out.append(f"### Hits: {name}")
            if not hits[name]:
                out.append("_none_")
            else:
                for ln, txt in hits[name][:80]:
                    out.append(f"- line {ln}: `{txt}`")
                if len(hits[name]) > 80:
                    out.append(f"- ... ({len(hits[name]) - 80} more)")
            out.append("")

        dump("toplevel")
        dump("center")
        dump("geometry")
        dump("restored_flag")

    DOCS.mkdir(parents=True, exist_ok=True)
    rp = DOCS / f"Report_{RID}_Docking_ToplevelScan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    rp.write_text("\n".join(out), encoding="utf-8")
    print(f"[{RID}] OK: Report {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
