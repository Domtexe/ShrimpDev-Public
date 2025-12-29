# R2853 - READ-ONLY: Pipeline P3 Audit
# - Scans docs/PIPELINE.md
# - Extracts P3 tasks (- [ ] / - [x]) with "(P3)"
# - Classifies: NOTE / TODO / OBSOLETE / MERGE (suggested)
# - Writes a report to Reports/Report_R2853_YYYYMMDD_HHMMSS.md
# - Does NOT modify PIPELINE.md

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


EXIT_OK = 0
EXIT_FAIL = 11


@dataclass
class TaskItem:
    lineno: int
    done: bool
    raw: str
    kind: str  # NOTE / TODO / OBSOLETE / MERGE
    merge_key: str
    reasons: List[str]


TASK_RE = re.compile(r"^\s*-\s*\[(?P<done>[ xX])\]\s*(?P<rest>.*)$")
HAS_P3_RE = re.compile(r"\(P3\)")
SRC_RE = re.compile(r"\(src:.*?\)")
PATH_RE = re.compile(r"[A-Za-z]:\\[^)\s]+|[A-Za-z]:/[^)\s]+")
CODETICK_RE = re.compile(r"`([^`]*)`")
WS_RE = re.compile(r"\s+")

OBSOLETE_HINTS = [
    "obsolete",
    "obsolet",
    "overflüssig",
    "no-op",
    "already",
    "already adjusted",
    "already fixed",
    "not found (maybe already adjusted)",
    "exists but is obsolete",
]


def _now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def _find_repo_root(arg_root: str | None) -> Path:
    if arg_root:
        return Path(arg_root).resolve()
    # fallback: assume tools/ next to this file
    return Path(__file__).resolve().parents[1]


def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def _normalize_for_merge(s: str) -> str:
    t = s
    # strip "(src:...)" blocks
    t = SRC_RE.sub("", t)
    # strip paths
    t = PATH_RE.sub("", t)
    # strip code ticks but keep content
    t = CODETICK_RE.sub(r"\1", t)
    # remove quotes/markdown emphasis noise
    t = t.replace("**", "").replace("__", "").replace("*", "")
    # compress whitespace
    t = WS_RE.sub(" ", t).strip().lower()
    # remove trailing punctuation clutter
    t = t.strip(" .,:;()-[]")
    return t


def _classify(raw: str, done: bool) -> Tuple[str, List[str]]:
    r = raw.strip()
    r_low = r.lower()

    reasons: List[str] = []

    # Base by tag presence
    if " note" in r_low or r_low.startswith("(p3) note") or "(p3) note" in r_low:
        kind = "NOTE"
        reasons.append("Contains NOTE marker")
    elif " todo" in r_low or r_low.startswith("(p3) todo") or "(p3) todo" in r_low:
        kind = "TODO"
        reasons.append("Contains TODO marker")
    else:
        # default: task without explicit note/todo → treat as TODO
        kind = "TODO"
        reasons.append("No explicit NOTE/TODO marker → default TODO")

    # Obsolete hints (never auto-mark done; only suggest)
    for h in OBSOLETE_HINTS:
        if h in r_low:
            kind = "OBSOLETE"
            reasons.append(f'Obsolete hint: "{h}"')
            break

    # If already done, keep kind but annotate
    if done:
        reasons.append("Already checked [x] in pipeline")

    return kind, reasons


def _extract_p3_tasks(lines: List[str]) -> List[Tuple[int, bool, str]]:
    items: List[Tuple[int, bool, str]] = []
    for i, line in enumerate(lines, start=1):
        m = TASK_RE.match(line)
        if not m:
            continue
        rest = m.group("rest")
        if not HAS_P3_RE.search(rest):
            continue
        done = (m.group("done").strip().lower() == "x")
        items.append((i, done, rest.rstrip()))
    return items


def _build_merge_groups(tasks: List[TaskItem]) -> Dict[str, List[TaskItem]]:
    groups: Dict[str, List[TaskItem]] = {}
    for t in tasks:
        groups.setdefault(t.merge_key, []).append(t)
    # keep only duplicates
    return {k: v for k, v in groups.items() if len(v) > 1}


def _render_report(
    repo: Path,
    pipeline_path: Path,
    tasks: List[TaskItem],
    merge_groups: Dict[str, List[TaskItem]],
    out_path: Path,
) -> str:
    total = len(tasks)
    open_count = sum(1 for t in tasks if not t.done)
    done_count = total - open_count

    by_kind: Dict[str, int] = {}
    for t in tasks:
        by_kind[t.kind] = by_kind.get(t.kind, 0) + 1

    lines: List[str] = []
    lines.append(f"# R2853 - Pipeline P3 Audit (READ-ONLY)")
    lines.append("")
    lines.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"- Repo: `{repo}`")
    lines.append(f"- Pipeline: `{pipeline_path}`")
    lines.append(f"- Report: `{out_path}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total P3 tasks found: **{total}**")
    lines.append(f"- Open: **{open_count}**")
    lines.append(f"- Done: **{done_count}**")
    lines.append("")
    lines.append("### Classification counts (suggested)")
    lines.append("")
    for k in ["TODO", "NOTE", "OBSOLETE", "MERGE"]:
        if k in by_kind:
            lines.append(f"- {k}: **{by_kind[k]}**")
    lines.append("")
    lines.append("## P3 Tasks (line-by-line)")
    lines.append("")
    lines.append("> Legend: `NOTE/TODO/OBSOLETE/MERGE` are **suggestions**; R2853 does not edit PIPELINE.md.")
    lines.append("")

    # mark merge candidates
    merge_keys = set(merge_groups.keys())
    for t in tasks:
        if t.merge_key in merge_keys:
            # only override if not OBSOLETE (obsoletes can also duplicate)
            if t.kind != "OBSOLETE":
                t.kind = "MERGE"
                if "Duplicate/merge candidate" not in t.reasons:
                    t.reasons.append("Duplicate/merge candidate")

    for t in tasks:
        chk = "x" if t.done else " "
        lines.append(f"- L{t.lineno:04d} `[{chk}]` **{t.kind}** — {t.raw}")
        if t.reasons:
            lines.append(f"  - reasons: " + "; ".join(t.reasons))
    lines.append("")

    if merge_groups:
        lines.append("## Merge candidates (duplicate-like groups)")
        lines.append("")
        for idx, (k, group) in enumerate(merge_groups.items(), start=1):
            lines.append(f"### Group {idx}")
            lines.append("")
            # show normalized key safely (short)
            key_preview = (k[:180] + "…") if len(k) > 180 else k
            lines.append(f"- normalized key: `{key_preview}`")
            lines.append("")
            for t in group:
                chk = "x" if t.done else " "
                lines.append(f"  - L{t.lineno:04d} `[{chk}]` {t.raw}")
            lines.append("")
    else:
        lines.append("## Merge candidates")
        lines.append("")
        lines.append("- None detected by simple normalization (manual review still recommended).")
        lines.append("")

    lines.append("## Next Step (recommended)")
    lines.append("")
    lines.append("- Create **R2854 (SAFE PATCH)** to apply chosen P3 consolidation decisions:")
    lines.append("  - convert pure notes into non-task text blocks (keep content)")
    lines.append("  - merge duplicates into single canonical tasks")
    lines.append("  - mark truly obsolete items as `[x]` with a short reason")
    lines.append("")

    return "\n".join(lines) + "\n"


def main() -> int:
    repo = _find_repo_root(sys.argv[1] if len(sys.argv) > 1 else None)

    pipeline_path = repo / "docs" / "PIPELINE.md"
    if not pipeline_path.exists():
        # also allow alternate location if someone passed a direct path in env
        alt = Path(str(pipeline_path)).resolve()
        print(f"[R2853] ERROR: PIPELINE.md not found at: {pipeline_path}")
        return EXIT_FAIL

    reports_dir = repo / "Reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    out_path = reports_dir / f"Report_R2853_{_now_stamp()}.md"

    txt = _read_text(pipeline_path)
    raw_lines = txt.splitlines()

    extracted = _extract_p3_tasks(raw_lines)

    tasks: List[TaskItem] = []
    for lineno, done, rest in extracted:
        kind, reasons = _classify(rest, done)
        merge_key = _normalize_for_merge(rest)
        tasks.append(TaskItem(lineno=lineno, done=done, raw=rest, kind=kind, merge_key=merge_key, reasons=reasons))

    merge_groups = _build_merge_groups(tasks)

    report_txt = _render_report(repo, pipeline_path, tasks, merge_groups, out_path)
    out_path.write_text(report_txt, encoding="utf-8", errors="replace")

    print(f"[R2853] OK: Report: {out_path}")
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
