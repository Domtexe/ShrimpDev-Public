# -*- coding: utf-8 -*-
"""
[R2387] READ-ONLY:
- Parse ShrimpDev.ini and dump [Docking] essentials
- Grep codebase for write entrypoints (config_loader.save, ini_writer usage, configparser.write)
Writes report to docs/.
"""

from __future__ import annotations
from pathlib import Path
from datetime import datetime
import configparser
import re
import hashlib

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
INI = ROOT / "ShrimpDev.ini"

KEYS = ["main", "pipeline", "log", "runner_products"]

DENY_DIRS = {".git", "__pycache__", "_Archiv"}

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def is_denied(p: Path) -> bool:
    parts = {x.lower() for x in p.parts}
    return any(d.lower() in parts for d in DENY_DIRS)

def main() -> int:
    DOCS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = DOCS / f"Report_R2387_Docking_INI_WriteAudit_{stamp}.md"

    lines = []
    lines.append("# Report R2387 – Docking INI Presence + Write-Audit (READ-ONLY)")
    lines.append("")
    lines.append(f"- Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- Root: `{ROOT}`")
    lines.append("")

    # --- INI dump ---
    lines.append("## ShrimpDev.ini Status")
    if not INI.exists():
        lines.append(f"- INI: `{INI}` **NICHT gefunden**")
        report.write_text("\n".join(lines), encoding="utf-8")
        print(f"[R2387] FEHLER: INI fehlt: {INI}")
        return 2

    lines.append(f"- INI: `{INI}`")
    lines.append(f"- Size: {INI.stat().st_size} bytes")
    lines.append(f"- SHA256: `{sha256(INI)}`")
    lines.append("")

    cfg = configparser.ConfigParser()
    try:
        cfg.read(INI, encoding="utf-8")
    except Exception as e:
        lines.append(f"- Parse: FAIL: `{e!r}`")
        report.write_text("\n".join(lines), encoding="utf-8")
        print(f"[R2387] FEHLER: INI parse fail: {e!r}")
        return 3

    has_docking = cfg.has_section("Docking")
    lines.append(f"- Has [Docking]: **{has_docking}**")
    if has_docking:
        # show a compact dump
        items = sorted(cfg.items("Docking"))
        lines.append(f"- Docking keys count: {len(items)}")
    lines.append("")

    lines.append("## Docking Keys (expected)")
    if not has_docking:
        lines.append("_[Docking] fehlt komplett → Start muss zentrieren (Root cause sehr wahrscheinlich)._")
    else:
        for k in KEYS:
            g = cfg.get("Docking", f"{k}.geometry", fallback="").strip()
            op = cfg.get("Docking", f"{k}.open", fallback="").strip()
            dk = cfg.get("Docking", f"{k}.docked", fallback="").strip()
            ts = cfg.get("Docking", f"{k}.ts", fallback="").strip()
            lines.append(f"- `{k}`: open=`{op}` docked=`{dk}` geo=`{g}` ts=`{ts}`")
    lines.append("")

    # --- Write-audit grep ---
    lines.append("## Write-Audit (Code Grep)")
    patterns = {
        "config_loader.save": re.compile(r"\bconfig_loader\.save\s*\(", re.IGNORECASE),
        "ini_writer.merge_write_ini": re.compile(r"\bmerge_write_ini\s*\(", re.IGNORECASE),
        "configparser.write": re.compile(r"\.write\s*\(\s*.*\)", re.IGNORECASE),
        "open(..., 'w')": re.compile(r"open\s*\(.*,\s*['\"]w['\"]", re.IGNORECASE),
        "Path.write_text": re.compile(r"\.write_text\s*\(", re.IGNORECASE),
    }

    hits = {k: [] for k in patterns.keys()}
    py_files = []
    for p in (ROOT / "modules").rglob("*.py"):
        if is_denied(p):
            continue
        py_files.append(p)
    # include main_gui too
    py_files.append(ROOT / "main_gui.py")

    for p in sorted(set(py_files)):
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for name, rx in patterns.items():
            for i, line in enumerate(txt.splitlines(), 1):
                if rx.search(line):
                    hits[name].append((str(p.relative_to(ROOT)), i, line.strip()))

    for name in patterns.keys():
        lines.append(f"### {name}")
        if not hits[name]:
            lines.append("_keine Treffer_")
        else:
            for rel, ln, l in hits[name][:200]:
                lines.append(f"- {rel}:{ln}: `{l}`")
        lines.append("")

    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"[R2387] OK: Report geschrieben: {report}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
