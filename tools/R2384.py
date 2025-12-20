# -*- coding: utf-8 -*-
"""
[R2384] READ-ONLY Hook Scan for Docking:
Find concrete hook locations for:
- where undocked windows are created for keys: runner_products/log/pipeline
- where close handlers are attached (WM_DELETE_WINDOW / protocol / destroy / withdraw)
- where restore runs on startup / restart
- where geometry/centering happens
Writes a focused report to docs/.
NO MODIFICATIONS.
"""

from __future__ import annotations
from pathlib import Path
from datetime import datetime
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

KEYS = ["runner_products", "log", "pipeline"]

# Prioritized scan targets to keep report usable (we avoid _Archiv noise)
PREFER = [
    ROOT / "main_gui.py",
    ROOT / "modules",
]

DENY_DIRS = {
    "_Archiv",
    ".git",
    "__pycache__",
}

PATTERNS = {
    "Key mentions": r"(runner_products|log|pipeline)",
    "Docking module refs": r"(\bDocking\b|ui_dock|dock|undock|undocked|panel|toplevel)",
    "Create/show window": r"(Toplevel\(|create_.*window|open_.*window|show_.*window|deiconify\(|lift\(|transient\()",
    "Restore/startup": r"(restore|load_.*dock|apply_.*dock|init_.*dock|startup|on_start|restart)",
    "Close hooks": r"(WM_DELETE_WINDOW|protocol\(|on_close|close_window|destroy\(|withdraw\()",
    "Geometry/centering": r"(geometry\(|wm_geometry|center|centre|winfo_screenwidth|winfo_screenheight)",
    "INI calls": r"(config_manager|get_config|ShrimpDevConfigManager|ini_writer|merge_write_ini|save\()",
}

def is_denied(path: Path) -> bool:
    parts = {p.lower() for p in path.parts}
    return any(d.lower() in parts for d in DENY_DIRS)

def scan_files() -> list[Path]:
    out: list[Path] = []
    for base in PREFER:
        if base.is_file() and base.suffix == ".py":
            out.append(base)
            continue
        if base.is_dir():
            for p in base.rglob("*.py"):
                if is_denied(p):
                    continue
                out.append(p)
    # stable order
    out = sorted(set(out))
    return out

def hit_lines(text: str, rx: re.Pattern) -> list[tuple[int, str]]:
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        if rx.search(line):
            hits.append((i, line.rstrip()))
    return hits

def main() -> int:
    DOCS.mkdir(parents=True, exist_ok=True)

    files = scan_files()
    compiled = {k: re.compile(v, re.IGNORECASE) for k, v in PATTERNS.items()}

    # First pass: only files that mention at least one KEY
    interesting: list[Path] = []
    for f in files:
        try:
            txt = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        if compiled["Key mentions"].search(txt):
            interesting.append(f)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = DOCS / f"Report_R2384_Docking_HookScan_{stamp}.md"

    lines: list[str] = []
    lines.append("# Report R2384 – Docking Hook-Scan (READ-ONLY)")
    lines.append("")
    lines.append(f"- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- Root: `{ROOT}`")
    lines.append(f"- Files scanned (preferred set): {len(files)}")
    lines.append(f"- Files mentioning keys: {len(interesting)}")
    lines.append("")
    lines.append("## Fokus-Keys")
    for k in KEYS:
        lines.append(f"- `{k}`")
    lines.append("")

    if not interesting:
        lines.append("## Ergebnis")
        lines.append("_Keine Treffer in bevorzugten Codepfaden. (Unerwartet)_")
        report.write_text("\n".join(lines), encoding="utf-8")
        print(f"[R2384] WARN: No key mentions found. Report: {report}")
        return 1

    # For each interesting file: show compact grouped hits
    for f in interesting:
        rel = f.relative_to(ROOT)
        try:
            txt = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        lines.append(f"## {rel}")
        # keep it focused: only include sections that actually hit
        for section in [
            "Key mentions",
            "Docking module refs",
            "Create/show window",
            "Restore/startup",
            "Close hooks",
            "Geometry/centering",
            "INI calls",
        ]:
            rx = compiled[section]
            hits = hit_lines(txt, rx)
            if not hits:
                continue
            lines.append(f"### {section}")
            for ln, ltxt in hits[:160]:
                lines.append(f"- line {ln}: `{ltxt}`")
            lines.append("")
        lines.append("")

    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"[R2384] OK: Report geschrieben: {report}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
