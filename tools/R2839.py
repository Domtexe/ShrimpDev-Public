# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List, Set, Tuple
import re
import shutil


RUNNER_ID = "R2839"


def now() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def write_report(repo: Path, lines: List[str]) -> Path:
    rp = repo / "Reports"
    ensure_dir(rp)
    out = rp / f"Report_{RUNNER_ID}_{now()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")
    return out


def backup(repo: Path, target: Path) -> Path:
    arch = repo / "_Archiv"
    ensure_dir(arch)
    bak = arch / f"{target.name}.{RUNNER_ID}_{now()}.bak"
    shutil.copy2(target, bak)
    return bak


RUNNER_STEM_RE = re.compile(r"^(R\d{4,})$", re.IGNORECASE)
RUNNER_FILE_RE = re.compile(r"^(R\d{4,})\.(cmd|py)$", re.IGNORECASE)
RUNNER_TOOLS_RE = re.compile(r"^(tools[\\/])?(R\d{4,})(\.(cmd|py))?$", re.IGNORECASE)


def _variants(stem: str) -> List[str]:
    # Generate variants that cover typical purge comparisons:
    # - stem (R2691)
    # - name with ext (R2691.cmd / R2691.py)
    # - relpath tools\... (tools\R2691.cmd / tools\R2691.py)
    # - forward slash variants (tools/R2691.cmd etc.)
    stem = stem.upper()
    return [
        stem,
        f"{stem}.cmd",
        f"{stem}.py",
        f"tools\\{stem}.cmd",
        f"tools\\{stem}.py",
        f"tools/{stem}.cmd",
        f"tools/{stem}.py",
    ]


def main() -> int:
    repo = repo_root()
    report: List[str] = []
    report.append(f"# {RUNNER_ID} PATCH: Expand runner_whitelist variants")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Root: `{repo}`")
    report.append("")

    wl = repo / "registry" / "runner_whitelist.txt"
    if not wl.exists():
        report.append(f"ERROR: Missing `{wl}`")
        write_report(repo, report)
        return 11

    bak = backup(repo, wl)
    report.append(f"- Backup: `{bak}`")
    report.append("")

    raw_lines = wl.read_text(encoding="utf-8", errors="replace").splitlines()

    # Preserve comment/blank lines, but rebuild the entry set deterministically
    kept_non_entries: List[str] = []
    entries: List[str] = []
    for ln in raw_lines:
        s = ln.strip()
        if not s or s.startswith("#"):
            kept_non_entries.append(ln)
            continue
        entries.append(s)

    # Normalize & expand
    out_set: Set[str] = set()
    stems_seen: Set[str] = set()

    for e in entries:
        m_stem = RUNNER_STEM_RE.match(e)
        m_file = RUNNER_FILE_RE.match(e)
        m_tools = RUNNER_TOOLS_RE.match(e)

        if m_stem:
            stem = m_stem.group(1).upper()
            stems_seen.add(stem)
            for v in _variants(stem):
                out_set.add(v)
            continue

        if m_file:
            stem = m_file.group(1).upper()
            stems_seen.add(stem)
            # keep original and also add missing siblings/paths
            for v in _variants(stem):
                out_set.add(v)
            continue

        if m_tools:
            stem = m_tools.group(2).upper()
            stems_seen.add(stem)
            for v in _variants(stem):
                out_set.add(v)
            # also keep the exact original string, as-is
            out_set.add(e)
            continue

        # Unknown entry: keep as-is
        out_set.add(e)

    # Hard-protect the known wrappers (in case they were missing)
    for stem in ("R2691", "R2692"):
        for v in _variants(stem):
            out_set.add(v)

    # Compose output:
    # Keep original comments/blanks at top, then a clean sorted list of entries.
    header: List[str] = []
    # Keep any initial comment/blank block from the original
    i = 0
    while i < len(raw_lines):
        s = raw_lines[i].strip()
        if s == "" or s.startswith("#"):
            header.append(raw_lines[i])
            i += 1
        else:
            break

    # If original had no header, add one
    if not header:
        header = [
            "# runner_whitelist.txt",
            "# Entries are expanded by R2839 to cover stem/name/path comparisons.",
            "",
        ]

    expanded_entries = sorted(out_set, key=lambda x: (x.lower(), x))

    new_lines = header + expanded_entries + [""]

    wl.write_text("\n".join(new_lines), encoding="utf-8", errors="replace")

    report.append("## Result")
    report.append(f"- Unique entries written: **{len(expanded_entries)}**")
    report.append(f"- Stems seen: **{len(stems_seen)}**")
    report.append("")
    report.append("## Note")
    report.append("- This is a compatibility hardening: it makes any purge comparison strategy match.")
    report.append("- Next: run Purge Scan/Apply and confirm R2691/R2692 are KEEP.")
    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
