# -*- coding: utf-8 -*-
"""
R2869 PATCH: MasterRules + Pipeline (f-string safety + guard policy) — canonical paths
Root: repo root (parent of /tools)
Edits:
  - docs/Master/MasterRules_Syntax.md  (append/insert section)
  - docs/PIPELINE.md                  (add P1 TODO lines)
Safety:
  - creates timestamped .bak copies
  - idempotent: won't duplicate if markers exist
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


RUNNER_ID = "R2869"
NOW = datetime.now().strftime("%Y%m%d_%H%M%S")


@dataclass
class EditResult:
    path: Path
    changed: bool
    backup: Path | None
    note: str


def repo_root() -> Path:
    # tools/R2869.py -> tools -> root
    return Path(__file__).resolve().parents[1]


def die(msg: str, code: int = 11) -> None:
    print(f"[{RUNNER_ID}] ERROR: {msg}")
    raise SystemExit(code)


def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def write_text(p: Path, s: str) -> None:
    p.write_text(s, encoding="utf-8", newline="\n")


def backup_file(p: Path) -> Path:
    b = p.with_suffix(p.suffix + f".{RUNNER_ID}.{NOW}.bak")
    b.write_text(read_text(p), encoding="utf-8", newline="\n")
    return b


def ensure_file_exists(p: Path, hint: str) -> None:
    if not p.exists():
        die(f"File not found: {p}\nHint: {hint}")


def upsert_masterrules_syntax(p: Path) -> EditResult:
    """
    Insert a new section near end; do not duplicate if marker exists.
    """
    marker = "<!-- SHRIMPDEV_RULE_FSTRING_SAFETY -->"
    section = f"""
{marker}

## F-String Safety & Guard-Policy (CI-relevant)

**Warum:** Mehrfach gab es Crashes/CI-Fails durch f-strings mit **undefinierten Namen** (z. B. `name` statt `btn_name`)
oder durch **Backslashes in f-string expressions**.

### Regeln (verbindlich)
- In `f"..."` dürfen nur **sicher definierte** Namen verwendet werden (lokal, Parameter, `self.`-Attribute).
- **Nie** in f-string expressions `\\` / `.replace("\\\\", ...)` o. ä. verwenden.
  → Vorher in eine Variable berechnen, dann in den f-string einfügen.
- Logging/Debug-Helper müssen **alle** verwendeten Variablen als Parameter bekommen
  (kein “ich greife mal schnell auf `name` zu”, wenn es nicht existiert).
- Nach jeder Änderung an UI/Toolbar/Runnern: **Smoke-Test / compile** lokal + CI muss grün sein.

### Guard (Empfehlung / Standard-Workflow)
- Vor Push: **Lint-Guard “unknown identifiers in f-strings”** laufen lassen (Runner R2867).
- Wenn Guard anschlägt: Fix **vor** Push. Kein “wird schon” mehr.
""".lstrip("\n")

    original = read_text(p)
    if marker in original:
        return EditResult(p, False, None, "MasterRules_Syntax: marker already present (no change).")

    new = original.rstrip() + "\n\n" + section + "\n"
    b = backup_file(p)
    write_text(p, new)
    return EditResult(p, True, b, "MasterRules_Syntax: appended f-string safety section.")


def upsert_pipeline(p: Path) -> EditResult:
    """
    Add P1 TODO entries that the Pipeline tab will parse.
    """
    marker = "<!-- SHRIMPDEV_PIPELINE_FSTRING_GUARD -->"
    block = f"""
{marker}
(P1) TODO: (CI/Guard) Introduce/keep Lint-Guard for f-string unknown identifiers (Runner R2867) and run it before Push.
(P1) TODO: (UI) Add a toolbar button “Lint Guard (R2867)” near Push/Purge diagnostics; on click run R2867 and show latest report via popup helper.
(P1) TODO: (Docs) Canonical paths reminder: MasterRules live in docs/Master/*.md; pipeline is docs/PIPELINE.md. All doc-updates must target canonical files (no root MasterRules.md).
""".lstrip("\n")

    original = read_text(p)
    if marker in original:
        return EditResult(p, False, None, "PIPELINE: marker already present (no change).")

    new = original.rstrip() + "\n\n" + block + "\n"
    b = backup_file(p)
    write_text(p, new)
    return EditResult(p, True, b, "PIPELINE: appended f-string guard TODO block.")


def write_report(root: Path, results: list[EditResult]) -> Path:
    reports_dir = root / "Reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    rp = reports_dir / f"Report_{RUNNER_ID}_{NOW}.md"

    lines = []
    lines.append(f"# {RUNNER_ID} PATCH Report\n")
    lines.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    lines.append(f"- Root: `{root}`\n")
    lines.append("\n## Results\n")
    for r in results:
        lines.append(f"### {r.path}\n")
        lines.append(f"- Changed: `{r.changed}`\n")
        lines.append(f"- Backup: `{r.backup}`\n" if r.backup else "- Backup: `None`\n")
        lines.append(f"- Note: {r.note}\n\n")

    rp.write_text("".join(lines), encoding="utf-8", newline="\n")
    return rp


def main() -> int:
    root = repo_root()

    mr_syntax = root / "docs" / "Master" / "MasterRules_Syntax.md"
    pipeline = root / "docs" / "PIPELINE.md"

    ensure_file_exists(mr_syntax, "Expected canonical file under docs/Master/MasterRules_Syntax.md")
    ensure_file_exists(pipeline, "Expected canonical file under docs/PIPELINE.md")

    results: list[EditResult] = []
    results.append(upsert_masterrules_syntax(mr_syntax))
    results.append(upsert_pipeline(pipeline))

    report = write_report(root, results)
    print(f"[{RUNNER_ID}] OK: Report: {report}")

    # Exit 0 even if no changes; it's fine / idempotent
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as e:
        die(f"Unhandled exception: {e!r}", 11)
