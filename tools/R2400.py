from __future__ import annotations

from pathlib import Path
from datetime import datetime
import re
import hashlib

RID = "R2400"
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

TARGET_HINTS = (
    "ShrimpDev.ini",
    "CONFIG_FILENAME",
    "config_loader.save",
    "config_mgr",
    "cfg.write(",
    "open(",
    "Path(",
    "write_text(",
    "merge_write_ini",
)

WRITE_PATTERNS = [
    ("cfg.write", re.compile(r"\bcfg\.write\s*\(")),
    ("configparser.write", re.compile(r"\.write\s*\(\s*f\s*\)")),
    ("open_w", re.compile(r"open\s*\([^)]*['\"]w['\"]")),
    ("open_wb", re.compile(r"open\s*\([^)]*['\"]wb['\"]")),
    ("Path.write_text", re.compile(r"\.write_text\s*\(")),
    ("merge_write_ini", re.compile(r"\bmerge_write_ini\s*\(")),
    ("config_loader.save", re.compile(r"\bconfig_loader\.save\s*\(")),
]

def stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    h.update(p.read_bytes())
    return h.hexdigest()

def safe_read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""

def rel(p: Path) -> str:
    try:
        return str(p.relative_to(ROOT))
    except Exception:
        return str(p)

def scan_file(p: Path, text: str) -> dict:
    hits = {"file": rel(p), "size": p.stat().st_size, "sha256": sha256(p), "hits": []}
    lines = text.splitlines()
    for label, rx in WRITE_PATTERNS:
        for i, line in enumerate(lines, start=1):
            if rx.search(line):
                # Keep it short & useful
                snippet = line.strip()
                hits["hits"].append({"kind": label, "line": i, "text": snippet[:240]})
    return hits

def main() -> int:
    py_files = list((ROOT / "modules").rglob("*.py")) + [ROOT / "main_gui.py"]
    py_files = [p for p in py_files if p.exists()]

    report = []
    report.append(f"# Report {RID} – Remaining INI Writers Map (READ-ONLY)")
    report.append("")
    report.append(f"- Timestamp: {ts()}")
    report.append(f"- Root: `{ROOT}`")
    report.append(f"- Files scanned: {len(py_files)}")
    report.append("")

    all_hits = []
    for p in py_files:
        txt = safe_read(p)
        if not txt:
            continue
        # quick prefilter
        if not any(h in txt for h in TARGET_HINTS):
            # still scan for cfg.write/open('w') because those may be generic
            if "cfg.write" not in txt and "open(" not in txt and "write_text" not in txt and "merge_write_ini" not in txt:
                continue
        hits = scan_file(p, txt)
        if hits["hits"]:
            all_hits.append(hits)

    # Sort by number of hits desc
    all_hits.sort(key=lambda d: len(d["hits"]), reverse=True)

    # Summarize top risk candidates (overwrite writers)
    overwrite = []
    merge = []
    calls = []
    for h in all_hits:
        kinds = {x["kind"] for x in h["hits"]}
        if "merge_write_ini" in kinds:
            merge.append(h["file"])
        if "cfg.write" in kinds or "open_w" in kinds or "configparser.write" in kinds:
            overwrite.append(h["file"])
        if "config_loader.save" in kinds:
            calls.append(h["file"])

    report.append("## Summary")
    report.append(f"- Files with potential overwrite-writes: **{len(set(overwrite))}**")
    report.append(f"- Files using merge_write_ini: **{len(set(merge))}**")
    report.append(f"- Files calling config_loader.save: **{len(set(calls))}**")
    report.append("")

    if overwrite:
        report.append("### Overwrite-risk (cfg.write / open('w') / configparser.write)")
        for f in sorted(set(overwrite))[:30]:
            report.append(f"- `{f}`")
        if len(set(overwrite)) > 30:
            report.append(f"- ... +{len(set(overwrite)) - 30} more")
        report.append("")

    if merge:
        report.append("### Merge-writers (merge_write_ini)")
        for f in sorted(set(merge))[:30]:
            report.append(f"- `{f}`")
        if len(set(merge)) > 30:
            report.append(f"- ... +{len(set(merge)) - 30} more")
        report.append("")

    report.append("## Detailed Hits")
    for h in all_hits:
        report.append(f"### `{h['file']}`")
        report.append(f"- size: {h['size']} bytes")
        report.append(f"- sha256: `{h['sha256']}`")
        for x in h["hits"][:80]:
            report.append(f"- L{x['line']} [{x['kind']}] `{x['text']}`")
        if len(h["hits"]) > 80:
            report.append(f"- ... +{len(h['hits']) - 80} more")
        report.append("")

    out = DOCS / f"Report_{RID}_INI_Writers_{stamp()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(report) + "\n", encoding="utf-8")

    print(f"[{RID}] OK: Report {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
