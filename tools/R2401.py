from __future__ import annotations

from pathlib import Path
from datetime import datetime
import hashlib
import re

RID = "R2401"
ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

TARGETS = [
    ROOT / "modules" / "config_loader.py",
    ROOT / "modules" / "config_mgr.py",
    ROOT / "modules" / "ui_toolbar.py",
    ROOT / "modules" / "config_manager.py",
    ROOT / "modules" / "ini_writer.py",
]

RX_DEF_SAVE = re.compile(r"^\s*def\s+save\s*\(", re.M)
RX_CFG_WRITE = re.compile(r"\bcfg\.write\s*\(")
RX_OPEN_W = re.compile(r"open\s*\([^)]*['\"]w['\"]")
RX_CONFIGPARSER_WRITE = re.compile(r"\.write\s*\(\s*f\s*\)")
RX_MERGE_WRITE = re.compile(r"\bmerge_write_ini\s*\(")
RX_INI_PATH = re.compile(r"ShrimpDev\.ini|CONFIG_FILENAME|get_config_path", re.I)
RX_DOCKING = re.compile(r"\[Docking\]|Docking\.", re.I)
RX_LOGWINDOW = re.compile(r"\bLogWindow\b|\blog_window\b", re.I)

def ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

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

def find_def_blocks(text: str, def_name: str = "save") -> list[tuple[int, int]]:
    lines = text.splitlines()
    blocks = []
    for i, line in enumerate(lines, start=1):
        if re.match(rf"^\s*def\s+{re.escape(def_name)}\s*\(", line):
            start = i
            indent = len(line) - len(line.lstrip(" "))
            end = i
            for j in range(i + 1, len(lines) + 1):
                ln = lines[j - 1]
                if ln.strip() == "":
                    end = j
                    continue
                ind = len(ln) - len(ln.lstrip(" "))
                if ind <= indent and re.match(r"^\s*(def|class)\s+", ln):
                    break
                if ind <= indent and ln.strip().startswith("@"):
                    break
                end = j
            blocks.append((start, end))
    return blocks

def grep_hits(text: str) -> dict:
    lines = text.splitlines()
    hits = []
    for idx, ln in enumerate(lines, start=1):
        kinds = []
        if RX_CFG_WRITE.search(ln) or RX_CONFIGPARSER_WRITE.search(ln):
            kinds.append("cfg.write/configparser")
        if RX_OPEN_W.search(ln):
            kinds.append("open('w')")
        if RX_MERGE_WRITE.search(ln):
            kinds.append("merge_write_ini")
        if RX_INI_PATH.search(ln):
            kinds.append("ini_path")
        if RX_DOCKING.search(ln):
            kinds.append("docking")
        if RX_LOGWINDOW.search(ln):
            kinds.append("logwindow")
        if kinds:
            hits.append((idx, ",".join(kinds), ln.strip()[:260]))
    return {"hits": hits}

def main() -> int:
    report = []
    report.append(f"# Report {RID} – INI Writer Deep Scan (READ-ONLY)")
    report.append("")
    report.append(f"- Timestamp: {ts()}")
    report.append(f"- Root: `{ROOT}`")
    report.append("")

    for p in TARGETS:
        if not p.exists():
            report.append(f"## `{rel(p)}`")
            report.append("- MISSING")
            report.append("")
            continue

        txt = safe_read(p)
        report.append(f"## `{rel(p)}`")
        report.append(f"- size: {p.stat().st_size} bytes")
        report.append(f"- sha256: `{sha256(p)}`")

        blocks = find_def_blocks(txt, "save")
        report.append(f"- save() blocks found: **{len(blocks)}**")

        g = grep_hits(txt)
        report.append(f"- suspicious hits: **{len(g['hits'])}**")
        report.append("")

        if blocks:
            lines = txt.splitlines()
            report.append("### save() block excerpts")
            for (s, e) in blocks[:5]:
                report.append(f"- Lines {s}-{e}:")
                snippet = lines[s-1:e]
                for k, ln in enumerate(snippet, start=s):
                    report.append(f"  - L{k}: `{ln.rstrip()[:260]}`")
            if len(blocks) > 5:
                report.append(f"- ... +{len(blocks)-5} more save() blocks")
            report.append("")

        if g["hits"]:
            report.append("### grep hits")
            for (ln, kind, textline) in g["hits"][:120]:
                report.append(f"- L{ln} [{kind}] `{textline}`")
            if len(g["hits"]) > 120:
                report.append(f"- ... +{len(g['hits'])-120} more")
            report.append("")

    out = DOCS / f"Report_{RID}_INI_WriterDeepScan_{stamp()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"[{RID}] OK: Report {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
