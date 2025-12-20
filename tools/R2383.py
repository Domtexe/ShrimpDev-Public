# -*- coding: utf-8 -*-
"""
[R2383] READ-ONLY Docking Diagnose:
- Scan modules/ and main_gui.py for:
  - keys: runner_products, log, pipeline
  - auto-open lists / restore routines
  - center_window / geometry defaults
  - close handlers that might re-open on restart
Writes report to docs/.
NO MODIFICATION.
"""

from __future__ import annotations
from pathlib import Path
from datetime import datetime
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

SCAN_FILES = []
for p in [ROOT / "modules", ROOT]:
    if p.is_dir():
        SCAN_FILES += list(p.rglob("*.py"))

KEYS = ["runner_products", "log", "pipeline"]
PATTERNS = {
    "Key mentions": r"(runner_products|log|pipeline)",
    "Auto-open keywords": r"(auto[_-]?open|restore|undock|undocked|open_window|show_window|create_window|spawn|popup|toplevel)",
    "Center/Geometry": r"(center|centre|geometry\(|wm_geometry|winfo_screenwidth|winfo_screenheight)",
    "Close/Destroy": r"(WM_DELETE_WINDOW|protocol\(|on_close|destroy\(|withdraw\(|deiconify\()",
    "INI Docking sections": r"(\[Docking|\bDocking\b)",
}

def hit_lines(text: str, rx: re.Pattern) -> list[tuple[int, str]]:
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if rx.search(line):
            out.append((i, line.rstrip()))
    return out

def main() -> int:
    DOCS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = DOCS / f"Report_R2383_Docking_Diagnose_{stamp}.md"

    compiled = {k: re.compile(v, re.IGNORECASE) for k, v in PATTERNS.items()}

    lines = []
    lines.append("# Report R2383 – Docking Diagnose (READ-ONLY)")
    lines.append("")
    lines.append(f"- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- Root: `{ROOT}`")
    lines.append(f"- Scanned files: {len(SCAN_FILES)}")
    lines.append("")
    lines.append("## Fokus-Keys")
    for k in KEYS:
        lines.append(f"- `{k}`")
    lines.append("")

    for file in sorted(SCAN_FILES):
        try:
            txt = file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        # only include files with key mentions to keep report small
        if not compiled["Key mentions"].search(txt):
            continue

        rel = file.relative_to(ROOT)
        lines.append(f"## {rel}")
        for pname, rx in compiled.items():
            hits = hit_lines(txt, rx)
            if not hits:
                continue
            lines.append(f"### {pname}")
            for ln, ltxt in hits[:120]:
                lines.append(f"- line {ln}: `{ltxt}`")
            lines.append("")
        lines.append("")

    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"[R2383] OK: Report geschrieben: {report}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
