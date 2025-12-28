# -*- coding: utf-8 -*-
from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

RUNNER_ID = "R2854"
EXIT_FAIL = 11

TASK_RE = re.compile(r"^(\s*-\s*)\[(?P<done>[ xX])\](\s*)(?P<rest>.*)$")
HAS_P3_RE = re.compile(r"\(P3\)")

OBSOLETE_HINTS = [
    "obsolete",
    "obsolet",
    "overflüssig",
    "no-op",
    "already",
    "already fixed",
    "already adjusted",
    "not found (maybe already adjusted)",
    "exists but is obsolete",
]

def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def backup(repo: Path, target: Path) -> Path:
    arch = repo / "_Archiv"
    ensure_dir(arch)
    bak = arch / f"{target.name}.{RUNNER_ID}_{now_stamp()}.bak"
    shutil.copy2(target, bak)
    return bak

def write_report(repo: Path, lines: List[str]) -> Path:
    rp = repo / "Reports"
    ensure_dir(rp)
    out = rp / f"Report_{RUNNER_ID}_{now_stamp()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")
    return out

def classify_p3(rest: str) -> Tuple[str, List[str]]:
    """
    Returns: kind in {NOTE, TODO, OBSOLETE} and reasons
    """
    r = rest.strip()
    low = r.lower()
    reasons: List[str] = []

    # NOTE detection (explicit markers)
    if "(p3) note" in low or low.startswith("note") or " note:" in low or " note " in low:
        kind = "NOTE"
        reasons.append("NOTE marker")
    else:
        kind = "TODO"
        reasons.append("default TODO")

    for h in OBSOLETE_HINTS:
        if h in low:
            kind = "OBSOLETE"
            reasons.append(f'Obsolete hint "{h}"')
            break

    return kind, reasons

def main(root_arg: str) -> int:
    repo = Path(root_arg).resolve()
    report: List[str] = []
    report.append(f"# {RUNNER_ID} SAFE PATCH: Pipeline P3 Cleanup")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Root: `{repo}`")
    report.append("")

    pipe = repo / "docs" / "PIPELINE.md"
    if not pipe.exists():
        report.append(f"ERROR: Missing `{pipe}`")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return EXIT_FAIL

    bak = backup(repo, pipe)
    report.append(f"- Target: `{pipe}`")
    report.append(f"- Backup: `{bak}`")
    report.append("")

    original = pipe.read_text(encoding="utf-8", errors="replace")
    lines = original.splitlines()

    n_note = 0
    n_obsolete_closed = 0
    n_p3_seen = 0

    changed_lines: List[str] = []
    try:
        for line in lines:
            m = TASK_RE.match(line)
            if not m:
                changed_lines.append(line)
                continue

            done = (m.group("done").strip().lower() == "x")
            rest = m.group("rest")

            if not HAS_P3_RE.search(rest):
                changed_lines.append(line)
                continue

            n_p3_seen += 1
            kind, reasons = classify_p3(rest)

            # 1) NOTE: remove checkbox (becomes non-task line)
            if kind == "NOTE":
                # Convert "- [ ] ..." to "- NOTE: ..." (keeps content, no checkbox)
                # Preserve indentation/prefix
                prefix = m.group(1)  # "- " with indentation
                new_line = f"{prefix}NOTE: {rest}".rstrip()
                changed_lines.append(new_line)
                n_note += 1
                continue

            # 2) OBSOLETE: mark done if not already
            if kind == "OBSOLETE" and not done:
                prefix = m.group(1)
                spacer = m.group(3)
                # Append short marker to avoid ambiguity; keep it minimal
                marker = " (auto-closed R2854: obsolete)"
                new_rest = rest if "auto-closed R2854" in rest else (rest + marker)
                changed_lines.append(f"{prefix}[x]{spacer}{new_rest}".rstrip())
                n_obsolete_closed += 1
                continue

            # 3) TODO or already-done OBSOLETE: keep as-is
            changed_lines.append(line)

        # Append a non-task summary block (no checkbox)
        summary = [
            "",
            "## R2854 Summary (auto)",
            f"- Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"- P3 items scanned: {n_p3_seen}",
            f"- P3 NOTE converted to non-tasks: {n_note}",
            f"- P3 OBSOLETE auto-closed: {n_obsolete_closed}",
        ]
        # Avoid duplicating if re-run
        if "## R2854 Summary (auto)" not in "\n".join(changed_lines):
            changed_lines.extend(summary)

        new_text = "\n".join(changed_lines) + "\n"
        pipe.write_text(new_text, encoding="utf-8", errors="replace")

        report.append("## Changes")
        report.append(f"- P3 scanned: **{n_p3_seen}**")
        report.append(f"- NOTE -> non-task: **{n_note}**")
        report.append(f"- OBSOLETE auto-closed: **{n_obsolete_closed}**")
        report.append("")
        report.append("## Notes")
        report.append("- No P3 TODO entries were altered.")
        report.append("- P3 NOTE entries remain as content, but no longer appear as tasks in the Pipeline tab.")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] OK -> {rp}")
        return 0

    except Exception as e:
        # Rollback to backup on any exception (MR)
        try:
            shutil.copy2(bak, pipe)
        except Exception:
            pass
        report.append(f"ERROR: Exception during patch: `{type(e).__name__}: {e}`")
        report.append("Rollback: restored from backup.")
        rp = write_report(repo, report)
        print(f"[{RUNNER_ID}] FAIL -> {rp}")
        return EXIT_FAIL

if __name__ == "__main__":
    import sys
    root = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parents[1])
    raise SystemExit(main(root))
