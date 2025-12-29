import sys
import re
from pathlib import Path
from datetime import datetime

RID = "R2810"


def ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def write_report(root: Path, content: str) -> Path:
    d = root / "Reports"
    d.mkdir(parents=True, exist_ok=True)
    rp = d / f"Report_{RID}_{ts()}.md"
    rp.write_text(content, encoding="utf-8")
    return rp


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def find_lines(txt: str, needles):
    res = []
    for i, l in enumerate(txt.splitlines(), start=1):
        low = l.lower()
        if any(n.lower() in low for n in needles):
            res.append((i, l.rstrip()))
    return res


def extract_fn(txt: str, fn_name: str):
    m = re.search(rf"(?m)^def\s+{re.escape(fn_name)}\s*\(\s*app\s*\)\s*:\s*$", txt)
    if not m:
        return None
    start = m.start()
    # next top-level def
    m2 = re.search(r"(?m)^def\s+\w+\s*\(", txt[m.end():])
    end = (m.end() + m2.start()) if m2 else len(txt)
    return txt[start:end]


def list_latest_reports(reports: Path, prefix: str, n=8):
    if not reports.exists():
        return []
    files = sorted(reports.glob(prefix), key=lambda p: p.stat().st_mtime, reverse=True)[:n]
    return [f.name for f in files]


def _md_escape_cell(s: str) -> str:
    # Keep it minimal: escape pipes and backticks so markdown table stays intact.
    s = s.replace("|", "\\|")
    s = s.replace("`", "\\`")
    return s


def main():
    root = Path(sys.argv[1]).resolve()
    lt = root / "modules" / "logic_tools.py"
    ut = root / "modules" / "ui_toolbar.py"
    la = root / "modules" / "logic_actions.py"
    reports = root / "Reports"

    out = []
    out.append(f"# {RID} READ-ONLY – Popup Trigger & Source Trace\n\n")
    out.append(f"Root: `{root}`\n\n")

    for p in (lt, ut, la):
        out.append(f"## File: `{p}`\n")
        if not p.exists():
            out.append("MISSING\n\n")
            continue

        txt = read(p)
        needles = [
            "_r1851_show_popup",
            "_wrap_with_led_and_report_popup",
            "_after_runner_show_report",
            "Purge Scan",
            "Purge Apply",
            "R2218",
            "R2224",
            "_r2787_last_md",
        ]
        hits = find_lines(txt, needles)
        if not hits:
            out.append("_No hits._\n\n")
        else:
            out.append("|Line|Hit|\n|---:|---|\n")
            for ln, line in hits[:200]:
                safe = _md_escape_cell(line)
                out.append(f"|{ln}|`{safe}`|\n")
            out.append("\n")

    # show purge function bodies
    if lt.exists():
        txt = read(lt)
        for fn in ("action_tools_purge_scan", "action_tools_purge_apply"):
            out.append(f"## logic_tools.{fn}() (excerpt)\n")
            blk = extract_fn(txt, fn)
            if not blk:
                out.append("NOT FOUND\n\n")
            else:
                lines = blk.splitlines()
                a = "\n".join(lines[:120])
                out.append(f"```python\n{a}\n```\n\n")

    out.append("## Latest candidate report files (Reports)\n\n")
    out.append("### Canonical MD\n")
    for name in list_latest_reports(reports, "Report_R2218_*.md") + list_latest_reports(reports, "Report_R2224_*.md"):
        out.append(f"- `{name}`\n")
    out.append("\n### Any TXT candidates\n")
    pats = ["R2218*.txt", "R2224*.txt", "Report_R2218_*.txt", "Report_R2224_*.txt"]
    anytxt = False
    for pat in pats:
        names = list_latest_reports(reports, pat, n=8)
        if names:
            anytxt = True
            out.append(f"**{pat}**\n")
            for n in names:
                out.append(f"- `{n}`\n")
            out.append("\n")
    if not anytxt:
        out.append("_No TXT candidates found._\n\n")

    rp = write_report(root, "".join(out))
    print(f"[{RID}] OK: Report: {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
