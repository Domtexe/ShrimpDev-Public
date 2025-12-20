from __future__ import annotations

from pathlib import Path
from datetime import datetime
import hashlib
import re

RID = "R2404"
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

FILES = [
    ROOT / "main_gui.py",
    ROOT / "modules" / "module_docking.py",
    ROOT / "modules" / "ui_runner_products_tab.py",
    ROOT / "modules" / "ui_pipeline_tab.py",
    ROOT / "modules" / "ui_log_tab.py",
    ROOT / "modules" / "ui_toolbar.py",
]

RX = [
    ("geometry_call", re.compile(r"\b(?:wm_)?geometry\s*\(")),
    ("after_idle_geo", re.compile(r"after_idle\s*\(\s*lambda[^\n]*geometry", re.I)),
    ("center_helper", re.compile(r"\b_center_window\b|\bCENTER_OVER_APP\b|\boffscreen\b", re.I)),
    ("restore_from_ini", re.compile(r"\brestore_from_ini\b|\b_restore_one\b|\bapply_ini_geometry\b", re.I)),
    ("withdraw_deiconify", re.compile(r"\bwithdraw\b|\bdeiconify\b|\blift\b", re.I)),
]

def ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except Exception:
        return str(p)

def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""

def main() -> int:
    report = []
    report.append(f"# Report {RID} – Post-Restore Geometry Setter Scan (READ-ONLY)")
    report.append("")
    report.append(f"- Timestamp: {ts()}")
    report.append(f"- Root: `{ROOT}`")
    report.append("")

    for p in FILES:
        rp = rel(p)
        report.append(f"## `{rp}`")
        if not p.exists():
            report.append("- MISSING")
            report.append("")
            continue
        txt = read(p)
        report.append(f"- size: {p.stat().st_size} bytes")
        report.append(f"- sha256: `{sha256(p)}`")

        lines = txt.splitlines()
        hits = []
        for i, ln in enumerate(lines, start=1):
            kinds = []
            for name, rx in RX:
                if rx.search(ln):
                    kinds.append(name)
            if kinds:
                # include a few lines of context marker heuristics
                hits.append((i, ",".join(kinds), ln.strip()[:260]))

        report.append(f"- hits: **{len(hits)}**")
        report.append("")
        if hits:
            report.append("### hits")
            for (i, kinds, ln) in hits[:200]:
                report.append(f"- L{i} [{kinds}] `{ln}`")
            if len(hits) > 200:
                report.append(f"- ... +{len(hits)-200} more")
        report.append("")

    out = DOCS / f"Report_{RID}_GeometrySetters_{stamp()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"[{RID}] OK: Report {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
