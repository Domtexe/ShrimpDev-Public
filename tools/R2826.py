# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List, Tuple


RUNNER_ID = "R2826"


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
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out


def scan_file(fp: Path) -> List[Tuple[int, str]]:
    hits = []
    try:
        lines = fp.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception:
        return hits

    for i, line in enumerate(lines, start=1):
        if (
            "_update_push_states" in line
            or "private_pushable" in line
            or "public_pushable" in line
            or "btn_push_private" in line
            or "btn_push_public" in line
            or ".config(" in line
            or "state=" in line
        ):
            hits.append((i, line.rstrip()))
    return hits


def main() -> int:
    repo = repo_root()
    report: List[str] = []

    report.append(f"# {RUNNER_ID} READ-ONLY Diagnose: Push Button Logic")
    report.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append(f"- Root: `{repo}`")
    report.append("")
    report.append("## Scope")
    report.append("- File: `modules/ui_toolbar.py`")
    report.append("- READ-ONLY (no changes)")
    report.append("")

    target = repo / "modules" / "ui_toolbar.py"
    if not target.exists():
        report.append("ERROR: modules/ui_toolbar.py not found")
        write_report(repo, report)
        return 11

    hits = scan_file(target)

    report.append("## Hits")
    report.append("")
    if not hits:
        report.append("- No relevant lines found (unexpected)")
    else:
        for lineno, text in hits:
            report.append(f"- L{lineno}: {text}")

    report.append("")
    report.append("## Summary")
    report.append(f"- Total hits: **{len(hits)}**")
    report.append("")
    report.append("## Next Step")
    report.append(
        "- Use the reported line numbers to choose **one single canonical place**\n"
        "  for Push-State logic and patch it safely (no string replace, no injection)."
    )
    report.append("")

    rp = write_report(repo, report)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
