# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List
import shutil

RUNNER_ID = "R2851"

CI_YAML = """name: CI

on:
  push:
    branches: [ "main" ]
  pull_request:

jobs:
  sanity:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Python syntax gate (py_compile)
        run: |
          python -m py_compile main_gui.py
          python -m compileall -q modules tools

      - name: CI sanity
        run: echo "CI OK"
"""

def now() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def backup(repo: Path, target: Path) -> Path:
    arch = repo / "_Archiv"
    ensure_dir(arch)
    bak = arch / f"{target.name}.{RUNNER_ID}_{now()}.bak"
    shutil.copy2(target, bak)
    return bak

def patch_ci(repo: Path, lines: List[str]) -> None:
    wf = repo / ".github" / "workflows" / "ci.yml"
    if not wf.exists():
        lines.append(f"- SKIP: `{wf}` not found")
        return
    bak = backup(repo, wf)
    wf.write_text(CI_YAML, encoding="utf-8", errors="replace")
    lines.append(f"- OK: `{wf}` patched (backup: `{bak}`)")

def write_report(repo: Path, lines: List[str]) -> Path:
    rp = repo / "Reports"
    ensure_dir(rp)
    out = rp / f"Report_{RUNNER_ID}_{now()}.md"
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", errors="replace")
    return out

def main() -> int:
    repo = Path(__file__).resolve().parent.parent
    lines: List[str] = []
    lines.append(f"# {RUNNER_ID} PATCH: CI Python syntax gate")
    lines.append(f"- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    lines.append("## Private repo")
    patch_ci(repo, lines)
    lines.append("")

    # Optional local public mirror
    pub = repo.parent / "ShrimpDev_PUBLIC_EXPORT"
    lines.append("## Public mirror (local)")
    if pub.exists():
        patch_ci(pub, lines)
    else:
        lines.append(f"- SKIP: `{pub}` not present locally")
    lines.append("")

    rp = write_report(repo, lines)
    print(f"[{RUNNER_ID}] OK -> {rp}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
